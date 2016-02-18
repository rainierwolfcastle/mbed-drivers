import argparse, requests, json, time, sys

def run(url, target, commands):
    repo_name = url.split('/')[-1].split('.')[0]
    print(repo_name)
    headers = {'Content-Type':'application/json'}
    data = {
        'vcs_url': url,
        'target': target,
        'commands': json.loads(commands),
        'repo_name': repo_name
    }
    response = requests.post('http://testbench.mbed.com/v1/jobs', headers=headers, data=json.dumps(data))
    print('Test submitted')
    body = response.json()
    id = str(body['id'])
    status = body['status']
    while status != 'success' and status != 'failed':
        time.sleep(1)
        response = requests.get('http://testbench.mbed.com/v1/jobs/' + id)
        body = response.json()
        status = body['status']
    for step in body['steps']:
        print(step['name'])
        print(step['messages'])
    if status == 'success':
        print('Test succeeded')
        sys.exit(0)
    else:
        print('Test failed')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    parser.add_argument('--target')
    parser.add_argument('--commands')
    args = parser.parse_args()
    run(args.url, args.target, args.commands)

if __name__ == '__main__':
    main()
