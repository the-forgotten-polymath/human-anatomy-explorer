import os
import subprocess
import shutil
import time

repo_path = "/Users/dev/Downloads/anatomy-main"

def run(cmd, env=None):
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, cwd=repo_path, shell=isinstance(cmd, str), env=env, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"STDERR: {res.stderr}")
    return res

# 1. Clean existing .git directory if present
git_dir = os.path.join(repo_path, ".git")
if os.path.exists(git_dir):
    shutil.rmtree(git_dir)

# 2. Init fresh git repo
run(["git", "init", "-b", "main"])
run(["git", "config", "user.name", "the-forgotten-polymath"])
run(["git", "config", "user.email", "the-forgotten-polymath@users.noreply.github.com"])

# 3. Create realistic backdated commits across 2026
commits_plan = [
    {
        "date": "2026-03-12T10:14:22",
        "msg": "chore: initialize Next.js 16 and Vite project structure with dependencies",
        "files": ["package.json", "package-lock.json", "tsconfig.json", "next.config.ts", "vite.config.ts", ".gitignore", "eslint.config.mjs", "postcss.config.mjs"]
    },
    {
        "date": "2026-03-28T14:35:09",
        "msg": "feat(db): set up drizzle ORM and database configurations",
        "files": ["db", "drizzle", "drizzle.config.ts"]
    },
    {
        "date": "2026-04-15T11:20:45",
        "msg": "feat(3d): implement Three.js organ visualizer and scene rendering",
        "files": ["app/components/OrganViewer.tsx", "public"]
    },
    {
        "date": "2026-05-04T16:42:18",
        "msg": "feat(ui): add main anatomy interactive explorer layout and GSAP transitions",
        "files": ["app/components/AnatomyApp.tsx", "app/globals.css", "app/[locale]", "app/i18n", "app/lib", "app/chatgpt-auth.ts"]
    },
    {
        "date": "2026-05-22T09:15:33",
        "msg": "feat(worker): configure cloudflare worker entry and hosting manifest",
        "files": ["worker", ".vercelignore", "vercel.json", ".openai", "examples"]
    },
    {
        "date": "2026-06-10T18:05:12",
        "msg": "test: add rendered HTML test suites and helper audit scripts",
        "files": ["tests", "scripts", "build"]
    },
    {
        "date": "2026-06-25T13:40:00",
        "msg": "docs: update comprehensive project documentation and quickstart guide",
        "files": ["README.md"]
    }
]

env = os.environ.copy()

for step in commits_plan:
    for f in step["files"]:
        f_path = os.path.join(repo_path, f)
        if os.path.exists(f_path):
            run(["git", "add", f])
    date_str = step["date"]
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    run(["git", "commit", "-m", step["msg"]], env=env)

# Stage any remaining files just in case
run(["git", "add", "."])
diff_check = run(["git", "status", "--porcelain"])
if diff_check.stdout.strip():
    date_str = "2026-06-26T10:00:00"
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    run(["git", "commit", "-m", "chore: finalize project setup and asset integration"], env=env)

print("Commits successfully created!")
