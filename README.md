# EMLParser-Analyser
A ReversingLabs Analyser for TheHive & Cortex with included report template.

## Installation
### Analyzer
1. Open Cortex-Analyzers/analyzers/
2. Make a new Directory called "EMLParserV2"
3. Copy the "EMLParserV2.json", "parse.py" and "Requirements.txt" files inside

### Template
1. Navigate to Cortex-Analyzers/thehive-templates
2. Create a new folder called "EMLParser_1_2"
3. Copy the "long.html" file there


## Configuration
1. Open Cortex,
2. Refresh your analysers
3. Enable "EMLParser_1_2"
4. Configure the rest as you would like.
5. Save
6. Open TheHive
7. Go To "Report Templates"
8. "View Template" on Long Template for ReversingLabs_1_1
9. Copy the contents of long.html in here and save.
10. Refresh your page.

## Notes
The analyser is configured to work without the use of the REGEX python library.
The EML Parser that comes bundled with TheHive relies on it and it seems to cause considerable problems with RHEL and some Linux environments where the library produces copious System Wheel issues.
This is essentially a workaround analyser to get things working at their most basic, you lose the IOC extracting as a result.