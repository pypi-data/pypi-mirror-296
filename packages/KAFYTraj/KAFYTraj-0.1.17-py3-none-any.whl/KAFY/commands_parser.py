import re
import sys
import json
import os
from KAFY.Pipeline import TrajectoryPipeline
from KAFY.models_loader import load_model_from_huggingface, load_model_from_file

# Project location default path set through environment variable (case-insensitive)
kafy_project_location = os.getenv("KAFY_PROJECT_LOCATION".upper(), "/KafyProject/")
"""
Global variable to define the project's root directory.

Users can update this variable to specify a custom location for their project data, models, and results.

Attributes:
    kafy_project_location (str): The path to the main project directory. Defaults to '/KafyProject/'.

Example:
    To change the project location:
    
    >>> export KAFY_PROJECT_LOCATION=/new/project/location
"""


def add_pretraining_data(data_location: str = "data_location.csv"):
    """
    Adds dataset to Trajectory store, to be used later to pretrain all models.

        Args:
            data_location (str): file path of data to be tokenized and added.

        Returns:
            None
    """
    global kafy_project_location
    pipeline = TrajectoryPipeline(
        mode="addingData",
        # use_tokenization=True,
        project_path=kafy_project_location,
    )
    trajectories_list = pipeline.get_trajectories_from_csv(data_location)
    pipeline.set_trajectories(trajectories_list)
    # TODO Youssef: This can be given from the user
    # pipeline.set_tokenization_resolution(10)
    pipeline.add_training_data()


def add_model(model_family, source, config_path, save_as_name):
    # @YOUSSEF DO: I need to use the optut_name to save the transformer_family using this name in the pyramid
    global kafy_project_location
    # If the model is available at HuggingFace then load it
    if source.lower() == "hf":
        model = load_model_from_huggingface(
            model_name=model_family, config_path=config_path
        )
    # or load it from a user-defined class
    else:
        ##This is not implemented for now
        model = load_model_from_file(source, config_path)

    pipeline = TrajectoryPipeline(
        mode="addModel",
        project_path=kafy_project_location,
    )
    # Pretrain logic
    # for every dataset in pretraining trajectory store:
    # Tokenize if not tokenized
    # Train model on data
    # Use Spatial Partioning to know MBR of data and save model in pretrained pyramid

    """
    # initialize the data collator, randomly masking 20% (default is 15%) of the tokens for the Masked Language
    # Modeling (MLM) task
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=True, mlm_probability=0.2
    )
    training_args = TrainingArguments(
    output_dir=model_path,          # output directory to where save model checkpoint
    evaluation_strategy="steps",    # evaluate each `logging_steps` steps
    overwrite_output_dir=True,
    num_train_epochs=1,            # number of training epochs, feel free to tweak
    per_device_train_batch_size=10, # the training batch size, put it as high as your GPU memory fits
    gradient_accumulation_steps=8,  # accumulating the gradients before updating the weights
    per_device_eval_batch_size=64,  # evaluation batch size
    logging_steps=1000,             # evaluate, log and save model checkpoints every 1000 step
    save_steps=1000,
    # load_best_model_at_end=True,  # whether to load the best model (in terms of loss) at the end of training
    # save_total_limit=3,           # whether you don't have much space so you let only 3 model weights saved in the disk
    )
    # initialize the trainer and pass everything to it
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
    )
    trainer.train()
    """
    # TODO: For now the model architecure will be added to TransformersPlugin/pretraining
    print(model)
    print(model.config)
    transformersPluginDirectory = os.path.join(
        kafy_project_location, "transformersPlugin"
    )
    if not os.path.exists(transformersPluginDirectory):
        os.makedirs(transformersPluginDirectory)
    # From HF utilities
    # But do I need to call the trainer before?
    model.save_pretrained(
        os.path.join(transformersPluginDirectory, "pretraining", save_as_name)
    )
    # Need also to work on the tokenizer.

    # Now after the model is saved, I need to load it and the tokenizer and start the pre
    # pretraining_datasets = []
    # for every_dataset in pretraining_datasets:
    #     # every_dataset this should be the name of the file of the dataset.
    #     trajectories_list = pipeline.get_trajectories_from_csv(file_path=every_dataset)
    #     pipeline.set_trajectories(trajectories_list)
    #     pipeline.set_tokenization_resolution(resolution=10)
    #     model_path, tokenized_dataset_path = pipeline.run()
    #     with open(config_path, "r", encoding="utf-8") as json_file:
    #         model_configs = json.load(json_file)
    #     # @YOUSSEF DO: I need to have a set of available models to check if he chose an existing architecture
    #     transformer_family = transformer_family.lower()

    #     model_configs["checkpoint_filepath"] = model_path
    #     model_configs["dataset_path"] = tokenized_dataset_path
    #     model_configs["output_dir"] = os.path.join(
    #         kafy_project_location, "temp_data_train_val_test"
    #     )
    #     print(model_configs)
    #     # TODO: we need to make a case swtich here of all supported families
    #     if transformer_family == "bert":
    #         # This should raise errors if chosen family is not sutiable with provided configs from researcher
    #         pretrain_BERT(model_configs)


def finetune_model(task, pretrained_model_path, config_path, output_name):
    # Initialize and run your fine-tuning pipeline here
    pipeline = TrajectoryPipeline(
        mode="finetuning",
        operation_type=task,
        # other relevant configurations
    )
    # Fine-tuning logic
    print(f"Fine-tuned model saved as {output_name}")


def summarize_data(data_path, model_path):
    # Initialize and run your summarization pipeline here
    pipeline = TrajectoryPipeline(
        mode="operation",
        operation_type="summarization",
        # other relevant configurations
    )
    # Summarization logic
    print("Summarization complete")


def parse_command(command=None):
    if command is None:
        command = " ".join(
            sys.argv[1:]
        )  # Join command-line arguments into a single string

    add_pretraining_data_command_match = re.match(
        r"(?i)add\s+data\s+from\s+(\S+)\s*",  # (?i) makes "add", "pretraining", "data", and "from" case-insensitive
        command,
    )
    # Captures HF or a model file and a config file
    add_model_match = re.match(
        r"(?i)add\s+model\s+(\w+)\s+from\s+(hf|(\S+))\s+using\s+(\S+)\s+as\s+(\S+)",
        command,
    )
    finetune_match = re.match(
        r"FINETUNE\s+(\w+)\s+FOR\s+(\w+)\s+USING\s+(\S+)\s+WITH\s+(\S+)\s+AS\s+(\S+)",
        command,
        re.IGNORECASE,
    )
    summarize_match = re.match(
        r"SUMMARIZE\s+FROM\s+(\S+)\s+USING\s+(\S+)", command, re.IGNORECASE
    )
    if add_pretraining_data_command_match:
        data_location = add_pretraining_data_command_match.group(1)
        add_pretraining_data(data_location)
    elif add_model_match:
        model_name = add_model_match.group(1)  # xBERT or model name
        source = add_model_match.group(2)  # "hf" or path to model.py
        config_path = add_model_match.group(4)  # Path to config.json
        save_as_name = add_model_match.group(5)  # Path to config.json
        add_model(model_name, source, config_path, save_as_name)
        print("New Model will be pretrained on all available datasets")
    elif finetune_match:
        model, task, pretrained_model, config, output_name = finetune_match.groups()
        finetune_model(task, pretrained_model, config, output_name)
    elif summarize_match:
        data, model = summarize_match.groups()
        summarize_data(data, model)
    else:
        raise ValueError("Command Not Supported (Erroneous Command)")
