# 1. Add a submodule (repo2) to your main repo (repo1)
git submodule add <repo2-url> <submodule-path>    # e.g., git submodule add https://github.com/user/repo2.git libs/repo2
git add .gitmodules <submodule-path>              # Stage submodule and config
git commit -m "Add repo2 as submodule"

# 2. Update submodule to the latest commit from its remote
git submodule update --remote <submodule-path>    # e.g., git submodule update --remote libs/repo2
git add <submodule-path>                          # Stage the updated submodule pointer
git commit -m "Update repo2 submodule"

# 3. Remove a submodule
git submodule deinit -f -- <submodule-path>       # e.g., git submodule deinit -f -- libs/repo2
git rm -f <submodule-path>                        # Also removes from index and .gitmodules
rm -rf .git/modules/<submodule-path>              # Clean up cached submodule data
git commit -m "Remove repo2 submodule"

# 4. Clone a repo with its submodules (all at once)
git clone --recurse-submodules <repo1-url>        # Clone main repo and all submodules

git pull --recurse-submodules

#    OR: Initialize and update submodules after cloning
git submodule update --init --recursive           # Fetch and checkout submodule code

# 5. Make and push changes in a submodule, then update pointer in parent
cd <submodule-path>
git add .                                        # Stage changes in submodule
git commit -m "Your commit in submodule"
git push                                         # Pushes to repo2 remote
cd ..                                            # Return to parent repo
git add <submodule-path>                         # Stage updated submodule pointer in repo1
git commit -m "Update submodule pointer"
git push                                         # Push pointer update to repo1 remote

# 6. Troubleshoot: If submodule folder is empty after clone/pull
git submodule update --init --recursive

# 7. Troubleshoot: If submodule is ignored, check .gitignore files
git check-ignore -v <submodule-path>