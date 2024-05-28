import os
import subprocess
import sys

ntfy_topic = os.environ["NTFY_TOPIC"]

words = sys.argv[1:]
sentence = "+".join(words)
sentence = sentence.replace("[", "_").replace("]", "_")

cmd = f'curl -d "{sentence}" ntfy.sh/{ntfy_topic}'

subprocess.check_call(cmd, shell=True)
print(f"Push notification <{sentence.replace('+', ' ')}> sent to ntfy topic.")
