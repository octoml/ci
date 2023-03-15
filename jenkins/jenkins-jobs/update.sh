#!/bin/bash
git clone https://opendev.org/jjb/jenkins-job-builder.git
cd jenkins-job-builder || exit 1
virtualenv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -r test-requirements.txt -e .
python jenkins_jobs/__main__.py --user tvm-bot --password "$1" --conf "/home/ubuntu/jenkins-jobs/$2/jenkins_jobs.ini" update "/home/ubuntu/jenkins-jobs/$2"

