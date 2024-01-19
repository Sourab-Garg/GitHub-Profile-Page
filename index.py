from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def get_github_data(username):
    user_url = f'https://api.github.com/users/{username}'
    repos_url = f'https://api.github.com/users/{username}/repos'

    user_data = requests.get(user_url).json()

    repo_data = requests.get(repos_url).json()

    return user_data, repo_data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        github_username = request.form['input_text']
    else:
        github_username = 'SourabGarg'
    user_data, repo_data = get_github_data(github_username)

    for repo in repo_data:
        repo_languages_url = repo['languages_url']
        response = requests.get(repo_languages_url)
        if response.status_code == 200:
            data = response.json()
            repo['all_languages'] = list(data.keys())
        else:
            print(f"Error: {response.status_code} - {response.text}")

    if user_data['name'] is None:
        return render_template("error.html")
    else:
        return render_template('index.html',
                               username=github_username,
                               user_data=user_data,
                               repo_data=repo_data)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
