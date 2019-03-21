# iOS-KnowledgeC-StructuredMetadata-Bplists
Script to extract compound bplists in the iOS -> KnowledgeC.db -> structuredmetadata table.

![alt text](run.PNG "Usage example")  

Usage: 
python ios_bplistinception.py /path/to/knowledgec.db iosversion [-d false]

1. Python 3
2. The ccl_bplist module is required for the scripts to work. It can be found here: https://github.com/cclgroupltd/ccl-bplist (But a version has been inluded in this repo)
3. The parse protobuf decoder by @Nevermoe (https://github.com/nevermoe/protobuf-decoder) has been updated to run on Python3 by Craig Rowland from Sandfly Security. This is to be placed in the same directory as the main script.
3. Export a knowledgeC database from iOS, if you place it in the same directory it will run, otherwise you can run the script and point it to the right path
4. Set the correct iOS version (11 or 12 supported). The script doesn't automatically identify which version of iOS the database has been extracted from.
5. Run the script. A timestamp named folder will be created that will contain two folders. One for extracted database content (named dirty) and one for the extracted bplist contained within the extracte database content (clean.)
6. Timestamped folder will also contain a HTML report with information on the clean bplists.

By default the tool will dump out the nsdata sections of the clean plists, you can turn this off with -d false, but I don't know why you would want to do that.

License: free to use etc, but if you're going to incorporate this into your paid tool and weren't before you read this code or the accompanying post please let me know or give credit.
