# execute in Doc repo
grep 'https://github.com/signalfx' $(find . -name README.md) | egrep -v 'https://github.com.signalfx/integrations' | grep -o 'https://github.com/signalfx/[^"#<)]*'
# or below:
grep -ho 'https://github.com/signalfx/[^"#<)/]*' $(find . -name README.md) | egrep -v "https://github.com/signalfx/integrations"