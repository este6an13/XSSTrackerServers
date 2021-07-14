init: sniffer_filterer html_parser
sniffer_filterer: sniffer_filterer.py
	mitmdump -s sniffer_filterer.py --set block_global=false &
html_parser: html_parser.py
	python3 html_parser.py
