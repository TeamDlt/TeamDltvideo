Python 3.10.0 (tags/v3.10.0:b494f59, Oct  4 2021, 19:00:18) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
name: Greetings

on: [pull_request, issues]

jobs:
  greeting:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
    steps:
    - uses: actions/first-interaction@v1
      with:
        repo-token: ${{ secrets.GITHUB_TOKEN }}
        issue-message: 'hello, thank you for reporting the issues that you have made, our developer team will immediately respond to it.'
        pr-message: 'hello, thank you for the pull request you have made, we are very happy if you can join us in developing this project through the pull request you made. ok, our developer team will respond to this soon.'
