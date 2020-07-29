zip lambda.zip *.py
mkdir packages
pip3 install jinja2 requests -t packages
cd packages
zip -ru ../lambda.zip *
