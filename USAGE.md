# Quick Usage Guide

## Basic Commands

### View user activity
```bash
python cli.py <username>
# or
./github-activity <username>
```

### Limit results
```bash
python cli.py octocat --limit 10
```

### Filter by event type
```bash
python cli.py torvalds --type PushEvent
```

### Show verbose details
```bash
python cli.py facebook --verbose
```

## Export Commands

### Export to JSON
```bash
python cli.py octocat --export json --output activity.json
```

### Export to CSV
```bash
python cli.py torvalds --export csv --output activity.csv
```

### Export with filters
```bash
python cli.py octocat --type PushEvent --limit 10 --export json --output pushes.json
```

## Event Types

You can filter by these event types:
- `PushEvent` - Push commits to repository
- `WatchEvent` - Star/unstar repository
- `IssuesEvent` - Create, edit, or close issues
- `PullRequestEvent` - Create, edit, or close pull requests
- `ForkEvent` - Fork repository
- `CreateEvent` - Create branch or tag
- `DeleteEvent` - Delete branch or tag
- `IssueCommentEvent` - Comment on issue
- `PullRequestReviewEvent` - Review pull request
- `ReleaseEvent` - Publish release
- `MemberEvent` - Add collaborator
- `PublicEvent` - Make repository public

## Advanced Examples

### Get only push events from last week
```bash
python cli.py username --type PushEvent --limit 20
```

### Export all starred repositories
```bash
python cli.py username --type WatchEvent --export csv --output stars.csv
```

### Get detailed verbose output
```bash
python cli.py username --verbose --limit 15
```

### Combined filters
```bash
python cli.py username --type PushEvent --limit 5 --verbose --export json --output data.json
```

## Help

For help and all available options:
```bash
python cli.py --help
```
