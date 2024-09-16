# actions
Composite Actions and Reusable workflows to commonly use

ci.yml requires:
```yaml
permissions:
  contents: read
```
If using the release part of the ci.yml workflow it requires:

```yaml
permissions:
  contents: read
  id-token: write
```

Using the release action requires:
```yaml
  permissions:
    id-token: write
```

To use the release part of the ci.yml workflow it requires
Adding the following trusted publisher to the pypi project at https://pypi.org/manage/project/[MY_PROJECT]/settings/publishing/

Owner: guywilsonjr
Repository name: actions
Workflow name: ci.yml

```yaml
permissions:
  id-token: write
```
