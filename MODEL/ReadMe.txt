FILE EXPLANATION: 

- Tutorial.mov is a video tutorial of the tool (please watch before use)

- My clippings.txt are my clippings. Upload yours to test it! There might be some problems if your kindle is set up in a different language (it will fail to parse the file). If it doesn't work with your clippings, please test it with my clippings.

- Clipping Display is the interface. It pools together all the functions from other files, and leverages the capabilities of streamlit to display the results.

- Libreria.py is the file where we parse the clippings and extract the info. (yes, sorry for writing stuff in Italian... libreria = bookshelf). It uses the file uploaded through streamlit (if there is a file), else it will try to use a local file, if there is the right path.

- filters.py is where there are all the nice filters to link quotes together. tfidf on title and on query (they are slightly different), doc2vec quote similarity etc.

- doc2vecmodel and ldamodel are the files where the model is trained (when you press 'set up' on streamlit interface). They output the model in tempDir, for later use. 

- tempDir is where we store files about usage (uploaded clippings, trained models etc).


HOW TO USE:

- watch Tutorial.mov 

- Open the folder in terminal and copy 'streamlit run clipping_display.py'

- set it up: if you are a previous user: click 'I am the last user' and input your name and surname: this will allow the model to retrieve your documents in tempDir. 

- for usage, refer to the video.

- Author, and Analytics are not still implemented (the button doesn't do anything).

NEXT:

- Implement Author filters and Analytics
- Improve topic recognition by cross filtering. Example: similar quotes + similar topics. (lda + doc2vec). 
- Improve Libreria.py to make it more adaptable to new clippings files. 