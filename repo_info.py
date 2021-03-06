from datetime import datetime, date


class RepoInfo:
    def __init__(self, r, configuration):
        self.gh_r = r
        self.config = configuration

    def get_name(self):
        return self.gh_r.name

    def get_html_url(self):
        return self.gh_r.html_url

    def get_lang(self):
        return self.gh_r.language

    def is_private(self):
        return self.gh_r.private

    def is_fork(self):
        return self.gh_r.fork

    def get_about(self):
        return self.gh_r.description

    def forks_count(self):
        return self.gh_r.forks_count

    def get_parent_name(self):
        if self.is_fork() and self.get_parent():
            return self.gh_r.parent.full_name
        return ""

    def get_parent(self):
        return self.gh_r.parent

    def wathers_count(self):
        return self.gh_r.watchers_count

    def get_pushed_date(self):
        return self.gh_r.pushed_at

    def get_created_at(self):
        return self.gh_r.owner.created_at

    def get_created_at_str(self):
        return self.get_created_at().strftime("%m/%d/%Y")

    def get_last_modified_str(self):
        # return self.gh_r.owner.last_modified
        return self.get_pushed_date().strftime("%m/%d/%Y")

    def get_watchers_count(self):
        return self.gh_r.watchers_count

    def get_stars(self):
        return self.gh_r.stargazers_count

    def get_stats(self):
        statistics = []
        stats = self.gh_r.get_stats_contributors()
        for stat in stats:
            author = str(stat.author)
            author = (author.replace('NamedUser(login="', "")).replace('")', "")
            for week in stat.weeks:

                if week.c != 0:
                    date = str(week.w)
                    date = date[:10]
                    statistics.append(
                        {
                            "author": author,
                            "date": date,
                            "added": week.a,
                            "deleted": week.d,
                            "changed": week.c,
                        }
                    )
        return statistics

    def get_team(self):
        repo2team = self.config.get("repo2team", {})
        if self.name in repo2team:
            return repo2team[self.name]

        p_team = self.get_potential_team()
        return f"{p_team} ?" if p_team else ""

    def get_potential_team(self):
        keyword2team = self.config.get("keyword2team", {})
        # TODO - do commit stats analysis
        for k, v in keyword2team.items():
            if self.name.find(k) != -1:
                return v
        lang2team = self.config.get("lang2team", {})
        if self.language in lang2team:
            return lang2team[self.language]
        return ""

    def get_potential_archive(self):
        today = datetime.now()
        last_chance_date = self.get_pushed_date()
        duration = today - last_chance_date
        return duration.days > 365

    def get_status(self):
        statuses = self.config["status"]
        if self.name in statuses:
            return statuses[self.name]
        return ""

    def get_doc_ref(self):
        doc_ref = self.config.get("docs_references", {})
        if self.name in doc_ref:
            return doc_ref[self.name]
        return ""

    name = property(get_name)
    url = property(get_html_url)
    language = property(get_lang)
    last_modified = property(get_last_modified_str)
    created = property(get_created_at_str)
    stars = property(get_stars)
    stats = property(get_stats)
    team = property(get_team)
    potential_team = property(get_potential_team)
    potential_archive = property(get_potential_archive)
    status = property(get_status)
    forks = property(get_parent_name)
    about = property(get_about)
    docref = property(get_doc_ref)
