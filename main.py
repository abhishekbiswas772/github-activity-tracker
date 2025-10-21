from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List
import requests
from requests.adapters import HTTPAdapter, Retry
from models import GitHubModel, GithubActor, GithubPayload, GithubRepo
from rich.table import Table
from rich.console import Console
import json
import csv
from event_formatter import get_event_description, get_event_icon

    

class GitHubActivityHandler:
    def __init__(self):
        self.session = requests.Session()
        self.retries = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        self.adapter = HTTPAdapter(max_retries=self.retries)
        self.session.mount("https://", self.adapter)
        self.session.mount("http://", self.adapter)
        self.github_base_uri = "https://api.github.com/users/"
        self.github_endpoint = "/events"
        self.console = Console()

        if not self.github_base_uri:
            raise self.GithubException("Github base url not found")
        
        if not self.github_endpoint:
            raise self.GithubException("Github activity endpoint not found")


    class GithubException(Exception):
        pass

    def parse_github_event(self, item: dict) -> GitHubModel:
        dt = datetime.strptime(item["created_at"], "%Y-%m-%dT%H:%M:%SZ")

        return GitHubModel(
            id=item.get("id"),
            type=item.get("type"),
            actor=GithubActor(
                id=item["actor"]["id"],
                login=item["actor"]["login"],
                display_login=item["actor"]["display_login"],
                gravatar_id=item["actor"].get("gravatar_id"),
                url=item["actor"]["url"],
                avatar_url=item["actor"]["avatar_url"],
            ),
            repo=GithubRepo(
                id=item["repo"]["id"],
                name=item["repo"]["name"],
                url=item["repo"]["url"],
            ),
            payload=GithubPayload(
                repository_id=item["payload"].get("repository_id"),
                push_id=item["payload"].get("push_id"),
                ref=item["payload"].get("ref"),
                head=item["payload"].get("head"),
                before=item["payload"].get("before"),
                description=item["payload"].get("description"),
            ),
            created_at=dt,
            public=item.get("public", True)
        )
    
    def parse_all_event(self, response_body):
        result = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(self.parse_github_event, item) for item in response_body]

            for future in as_completed(futures):
                try:
                    result_model = future.result()
                    result.append(result_model)
                except Exception as e:
                    print(f"Error parsing event: {e}")

        return result

    def get_github_user_activity(self, username: str) -> List[GitHubModel]:
        if not username:
            raise self.GithubException("Username not found, please send a valid one")
        try:
            final_url = f"{self.github_base_uri}{username}{self.github_endpoint}"
            if not final_url:
                raise self.GithubException("Github activity url not found")
            
            response = self.session.get(final_url)
            response.raise_for_status()
            if response.status_code == 200:
                response_bdy = response.json()
                result = self.parse_all_event(response_body=response_bdy)
                if not result:
                    return []
                return result
            else:
                raise self.GithubException("Cannot Parse User github activity")
        except Exception as e:
            raise self.GithubException(str(e))
        
    def to_cli_table(self, github_events: List[GitHubModel], verbose: bool = False):
        try:
            if not github_events:
                raise self.GithubException("Github events not found ...")
            table = Table(
                title="[bold cyan]GitHub Events[/bold cyan]",
                header_style="bold magenta",
                show_lines=True
            )

            if verbose:
                table.add_column("ID", style="cyan", width=12)

            table.add_column("Type", style="green", width=25)
            table.add_column("Actor", style="yellow", width=20)
            table.add_column("Repository", style="blue", width=30)
            table.add_column("Description", style="bright_white", width=35)
            table.add_column("Created At", style="white", width=20)

            if verbose:
                table.add_column("Public", style="red", width=8)

            for event in github_events:
                icon = get_event_icon(event.type)
                description = get_event_description(event)
                event_type_display = f"{icon} {event.type.replace('Event', '')}"

                row = []

                if verbose:
                    row.append(event.id)

                row.extend([
                    event_type_display,
                    event.actor.display_login,
                    event.repo.name,
                    description,
                    event.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                ])

                if verbose:
                    row.append("✅" if event.public else "❌")

                table.add_row(*row)

            self.console.print(table)

        except Exception as e:
            raise self.GithubException(str(e))

    def export_data(self, github_events: List[GitHubModel], format: str, output_path: str, verbose: bool = False):

        try:
            if not github_events:
                raise self.GithubException("No events to export")

            if format == "json":
                self._export_json(github_events, output_path, verbose)
            elif format == "csv":
                self._export_csv(github_events, output_path, verbose)
            else:
                raise self.GithubException(f"Unsupported export format: {format}")

        except Exception as e:
            raise self.GithubException(f"Export failed: {str(e)}")

    def _export_json(self, github_events: List[GitHubModel], output_path: str, verbose: bool):
        data = []
        for event in github_events:
            event_data = {
                "type": event.type,
                "actor": event.actor.display_login,
                "repository": event.repo.name,
                "description": get_event_description(event),
                "created_at": event.created_at.isoformat(),
            }

            if verbose:
                event_data.update({
                    "id": event.id,
                    "actor_id": event.actor.id,
                    "repo_id": event.repo.id,
                    "repo_url": event.repo.url,
                    "public": event.public,
                    "payload": {
                        "ref": event.payload.ref,
                        "head": event.payload.head,
                        "before": event.payload.before,
                    }
                })

            data.append(event_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _export_csv(self, github_events: List[GitHubModel], output_path: str, verbose: bool):
        fieldnames = ["type", "actor", "repository", "description", "created_at"]

        if verbose:
            fieldnames = ["id"] + fieldnames + ["repo_id", "public"]

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for event in github_events:
                row = {
                    "type": event.type,
                    "actor": event.actor.display_login,
                    "repository": event.repo.name,
                    "description": get_event_description(event),
                    "created_at": event.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }

                if verbose:
                    row.update({
                        "id": event.id,
                        "repo_id": event.repo.id,
                        "public": event.public,
                    })

                writer.writerow(row)

    @staticmethod
    def get_actions_factory(username: str):
        handler = GitHubActivityHandler()
        result = handler.get_github_user_activity(username=username)
        handler.to_cli_table(github_events=result)




        
    
    
