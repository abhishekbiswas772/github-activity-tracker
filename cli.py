#!/usr/bin/env python3
"""
GitHub Activity Tracker CLI
A command-line tool to fetch and display GitHub user activity.
"""

import sys
import argparse
from main import GitHubActivityHandler
from rich.console import Console
from rich.panel import Panel


console = Console()


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="github-activity",
        description="Fetch and display GitHub user activity in a beautiful table format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  github-activity abhishekbiswas772
  github-activity abhishekbiswas772 --limit 10
  github-activity abhishekbiswas772 --type PushEvent
  github-activity abhishekbiswas772 --export json --output activity.json
        """
    )

    parser.add_argument(
        "username",
        help="GitHub username to fetch activity for"
    )

    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=None,
        help="Limit the number of events to display (default: all)"
    )

    parser.add_argument(
        "-t", "--type",
        type=str,
        default=None,
        help="Filter by event type (e.g., PushEvent, IssuesEvent, WatchEvent)"
    )

    parser.add_argument(
        "-e", "--export",
        choices=["json", "csv"],
        help="Export data to file format"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output file path for export (required with --export)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed event information"
    )

    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Validate export arguments
    if args.export and not args.output:
        console.print("[red]Error:[/red] --output is required when using --export", style="bold")
        sys.exit(1)

    try:
        # Show loading message
        with console.status(f"[cyan]Fetching activity for user: {args.username}...", spinner="dots"):
            handler = GitHubActivityHandler()
            events = handler.get_github_user_activity(username=args.username)

        if not events:
            console.print(
                Panel(
                    f"[yellow]No activity found for user: {args.username}[/yellow]",
                    title="Info",
                    border_style="yellow"
                )
            )
            return

        # Apply filters
        if args.type:
            events = [e for e in events if e.type == args.type]
            if not events:
                console.print(
                    Panel(
                        f"[yellow]No events of type '{args.type}' found for user: {args.username}[/yellow]",
                        title="Info",
                        border_style="yellow"
                    )
                )
                return

        if args.limit:
            events = events[:args.limit]

        # Sort events by creation time (newest first)
        events.sort(key=lambda x: x.created_at, reverse=True)

        # Display results
        console.print(f"\n[bold green]Found {len(events)} event(s) for {args.username}[/bold green]\n")

        if args.export:
            handler.export_data(events, args.export, args.output, verbose=args.verbose)
            console.print(
                Panel(
                    f"[green]✓[/green] Data exported to: {args.output}",
                    title="Success",
                    border_style="green"
                )
            )
        else:
            handler.to_cli_table(github_events=events, verbose=args.verbose)

    except GitHubActivityHandler.GithubException as e:
        error_message = str(e)

        # Provide helpful error messages
        if "404" in error_message:
            console.print(
                Panel(
                    f"[red]User '{args.username}' not found on GitHub.[/red]\n"
                    f"Please check the username and try again.",
                    title="Error",
                    border_style="red"
                )
            )
        elif "403" in error_message:
            console.print(
                Panel(
                    f"[red]API rate limit exceeded.[/red]\n"
                    f"Please try again later or authenticate with a GitHub token.",
                    title="Error",
                    border_style="red"
                )
            )
        elif "Cannot Parse User github activity" in error_message:
            console.print(
                Panel(
                    f"[red]Failed to parse GitHub activity.[/red]\n"
                    f"This might be a temporary issue. Please try again.",
                    title="Error",
                    border_style="red"
                )
            )
        else:
            console.print(
                Panel(
                    f"[red]{error_message}[/red]",
                    title="Error",
                    border_style="red"
                )
            )
        sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)

    except Exception as e:
        console.print(
            Panel(
                f"[red]An unexpected error occurred:[/red]\n{str(e)}",
                title="Error",
                border_style="red"
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
