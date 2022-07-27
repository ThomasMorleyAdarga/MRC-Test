
=== Question Generation

1. Clone https://github.com/facebookresearch/XLM to the project.

2. Follow `QuestionGeneration/data_preparation.py` to prepare the training data. In the directory, `train_source_example_inputs.txt` gives samples in the source side, i.e., the narrative-style texts; `train_target_what_questions.txt` and `train_target_when_questions.txt` show samples in the target side, i.e., the query-style texts.

3. Train back-translation model to learn the mapping. `generated_questions.txt` gives the examples of the generated questions.


=== Question Answering

1. Follow `util.py` and `model_train_progressly.py` to preprocess the datasets and train the final model.



To get the model to acc work do:

1. Open Jupiter notebook inside of QuestionGeneration
Execute this:	
`%run data_generation.py`

2. Open Jupiter notebook inside of QuestionAnswering
Execute this:
`%pip install pytorch_transformers`

Then this:
`%conda install -c conda-forge allennlp -y`

Then is:
`%run reformat.py train.json test.json dev.json dataset`

For this to work the bert-large-cased-whole-word-masking-finetuned-squad needs to be in the same directory as the readme and the QuestionGeneration/QuestionAnswering folders (root directory)

The reformat script also expects our ACE data in the train.json/test.json/dev.json files

3. To train do this:
`%run model_train_progressly.py 1`



**Not sure where the trigger classification results are, or how the f1 is calculated - also, I think performance could be improved if we incorporate the FrameNet data**