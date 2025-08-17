import vk
from datetime import datetime
import re


class TccRubricFinder:
    def __init__(self):
        self.token_file = 'vk_token.txt'
        self.group_id = -19043  # Европа плюс group ID
        self.vk_api = None

    def authenticate_vk(self):
        with open(self.token_file, 'r') as file:
            token = file.read().strip()
        self.vk_api = vk.API(access_token=token, v='5.131')

    def parse_date_input(self, date_input):
        return datetime.strptime(date_input, "%Y-%m-%d").date()

    def fetch_posts(self, target_date):
        posts = self.vk_api.wall.get(owner_id=self.group_id, count=100)['items']
        for post in posts:
            post_date = datetime.fromtimestamp(post['date']).date()
            if post_date == target_date and "Top Club Chart" in post['text']:
                return post
        return None

    def fetch_comments(self, post_id):
        # Fetch the last 100 comments sorted by the latest
        comments = self.vk_api.wall.getComments(owner_id=self.group_id, post_id=post_id, count=100, sort='desc')[
            'items']
        sections = ["Резиденция", "Перспектива", "All Time Dance Anthem"]

        # Check if all three rubrics are present in the comment
        for comment in comments:
            if all(section in comment['text'] for section in sections):
                return comment['text']
        return None

    def extract_sections(self, comment_text, group_id, post_id):
        sections = ["Резиденция", "Перспектива", "All Time Dance Anthem"]
        result = {}
        for i, section in enumerate(sections):
            pattern = rf"{section}:(.*?)(?=\n{sections[i + 1]}:|\Z)" if i + 1 < len(sections) else rf"{section}:(.*)"
            match = re.search(pattern, comment_text, re.S)
            if match:
                tracks = [track.strip() for track in match.group(1).strip().split('\n') if track.strip()]
                if section == "Резиденция":
                    if len(tracks) >= 1 and '—' in tracks[0]:
                        parts = tracks[0].split('—', 1)
                        if len(parts) == 2:
                            result['residance_author'], result['residance_name'] = parts[0].strip(), parts[1].strip()
                        else:
                            raise RubricNotFoundError("Резиденция", group_id, post_id)
                    else:
                        raise RubricNotFoundError("Резиденция", group_id, post_id)
                elif section == "Перспектива":
                    if len(tracks) >= 1 and '—' in tracks[0]:
                        parts = tracks[0].split('—', 1)
                        if len(parts) == 2:
                            result['perspective_author'], result['perspective_name'] = parts[0].strip(), parts[
                                1].strip()
                        else:
                            raise RubricNotFoundError("Перспектива", group_id, post_id)
                    else:
                        raise RubricNotFoundError("Перспектива", group_id, post_id)
                elif section == "All Time Dance Anthem":
                    if len(tracks) >= 1 and '—' in tracks[0]:
                        parts = tracks[0].split('—', 1)
                        if len(parts) == 2:
                            # Remove year in parentheses
                            parts[1] = re.sub(r"\(\d{4}\)", "", parts[1]).strip()
                            result['alltime_author'], result['alltime_name'] = parts[0].strip(), parts[1].strip()
                        else:
                            raise RubricNotFoundError("All Time Dance Anthem", group_id, post_id)
                    else:
                        raise RubricNotFoundError("All Time Dance Anthem", group_id, post_id)
            else:
                raise RubricNotFoundError(section, group_id, post_id)
        return result

    def find_rubrics(self, target_date):
        self.authenticate_vk()

        # Fetch posts
        post = self.fetch_posts(target_date)
        if not post:
            return "No matching post found."

        # Fetch comments
        comment_text = self.fetch_comments(post['id'])
        if not comment_text:
            return "No suitable comment found."

        # Extract sections and tracks
        result = self.extract_sections(comment_text, self.group_id, post['id'])
        print('Found rubrics: ', result)

        return result


class RubricNotFoundError(Exception):
    def __init__(self, rubric_name, group_id, post_id):
        vk_post_url = f"https://vk.com/wall{group_id}_{post_id}"
        super().__init__(f"Rubric '{rubric_name}' not found in the comment. Please add them manually or check the post: {vk_post_url}")


if __name__ == "__main__":
    finder = TccRubricFinder()

    # Specify the date input
    date_input = "2025-07-26"  # Format: YYYY-MM-DD

    # Find and print the rubrics
    result = finder.find_rubrics(date_input)
    print(result)
