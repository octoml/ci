#!/usr/bin/env python3
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import os
import logging
from typing import Dict, Any, Optional, List

from .git_utils import GitHubRepo, DRY_RUN
from .github_commenter import BotCommentBuilder, Item
from .github_skipped_tests_comment import get_skipped_tests_comment
from .github_tag_teams import get_tags
from .github_docs_comment import get_doc_url
from .ci_runtime import ci_runtime_comment

PR_QUERY = """
    query ($owner: String!, $name: String!, $number: Int!) {
      repository(owner: $owner, name: $name) {
        pullRequest(number: $number) {
          title
          body
          state
          isDraft
          number
          baseRefOid
          author {
            login
          }
          labels(first:100) {
            nodes {
              name
            }
          }
          comments(last: 100) {
            pageInfo {
              hasPreviousPage
            }
            nodes {
              author {
                login
              }
              databaseId
              body
            }
          }
          commits(last: 1) {
            nodes {
              commit {
                oid
                statusCheckRollup {
                  contexts(first: 100) {
                    pageInfo {
                      hasNextPage
                    }
                    nodes {
                      ... on StatusContext {
                        state
                        context
                        targetUrl
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
"""


# TODO: These are all disabled for now, as they get ported over to lambda we can
# turn them back on
COMMENT_SECTIONS = {
    "ccs": lambda pr_data, github: get_tags(pr_data, github, team_issue=10317),
    "skipped-tests": lambda pr_data, github: get_skipped_tests_comment(
        pr_data, github=github
    ),
    "docs": lambda pr_data, github: get_doc_url(pr_data),
    "runtime": lambda pr_data, github: ci_runtime_comment(pr_data, github),
}


def github_pr_comment(
    webhook_pr_data: Dict[str, Any],
    user: str,
    repo: str,
    dry_run: bool,
    commenters: Optional[List[str]] = None,
):
    logger = logging.getLogger("py-github")
    test_data = None
    github = GitHubRepo(
        user=user,
        repo=repo,
        token=DRY_RUN if dry_run else os.environ["GITHUB_TOKEN"],
        test_data=test_data,
    )
    logger.info(f"Generated github: {github}")

    pr_data = github.graphql(
        PR_QUERY,
        {
            "owner": user,
            "name": repo,
            "number": webhook_pr_data["number"],
        },
    )

    pr_data = pr_data["data"]["repository"]["pullRequest"]
    commenter = BotCommentBuilder(github=github, data=pr_data)

    items = {}
    for key, generator in COMMENT_SECTIONS.items():
        if commenters is not None and key not in commenters:
            continue

        logging.info(f"Processing commenter: {key}")
        # Don't re-fetch items that have declared themselves done
        if not commenter.is_done(key):
            try:
                _, content = generator(pr_data, github)
                items[key] = Item(key=key, text=content, is_done=False)
            except Exception as e:
                logger.exception(e)

    logger.info(f"Commenting {len(items)} items: {items}")
    commenter.post_items(items=list(items.values()))
