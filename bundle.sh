zip lambda.zip *.py
mkdir -p packages
python3 -m pip install jinja2 requests -t packages
cd packages
zip -ru ../lambda.zip *
