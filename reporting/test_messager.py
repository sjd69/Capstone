import subprocess

with open('test_message.json', 'r') as msg_file:
    payload = msg_file.read().replace('\n', '')
    
# payload = '{"text":"TESTING, <@U751W3GQJ>", "username":"CI Testbot", "channel":"@U751W3GQJ"}'

webhook_url = "https://hooks.slack.com/services/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"

content_string = 'Content-Type:application/json'
print subprocess.check_output(["curl", "-X", "POST", "-H", content_string, "--data", payload, webhook_url])

