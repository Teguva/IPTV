import subprocess

def run_git_push():
    try:
        # Run git add, git commit, and git push
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Automated commit message'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)  # Replace 'main' with the correct branch name
        print("Changes pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    run_git_push()
input("Press Enter to exit...")