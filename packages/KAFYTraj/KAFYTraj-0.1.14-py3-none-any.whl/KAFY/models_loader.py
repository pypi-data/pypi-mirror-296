import importlib
import json
import inspect
import logging
import importlib.util
from transformers import *

# Define the model class mapping
MODEL_CLASS_MAPPING = {
    "albert": {"model_class": AlbertModel, "config_class": AlbertConfig},
    "bart": {"model_class": BartModel, "config_class": BartConfig},
    "bert": {"model_class": BertModel, "config_class": BertConfig},
    "bertgeneration": {
        "model_class": BertGenerationEncoder,
        "config_class": BertGenerationConfig,
    },
    "bigbird": {"model_class": BigBirdModel, "config_class": BigBirdConfig},
    "bigbirdpegasus": {
        "model_class": BigBirdPegasusModel,
        "config_class": BigBirdPegasusConfig,
    },
    "biogpt": {"model_class": BioGptModel, "config_class": BioGptConfig},
    "blenderbot": {"model_class": BlenderbotModel, "config_class": BlenderbotConfig},
    "blenderbotsmall": {
        "model_class": BlenderbotSmallModel,
        "config_class": BlenderbotSmallConfig,
    },
    "bloom": {"model_class": BloomModel, "config_class": BloomConfig},
    "camembert": {"model_class": CamembertModel, "config_class": CamembertConfig},
    "canine": {"model_class": CanineModel, "config_class": CanineConfig},
    "codegen": {"model_class": CodeGenModel, "config_class": CodeGenConfig},
    "convbert": {"model_class": ConvBertModel, "config_class": ConvBertConfig},
    "cpmannt": {"model_class": CpmAntModel, "config_class": CpmAntConfig},
    "ctrl": {"model_class": CTRLModel, "config_class": CTRLConfig},
    "deberta": {"model_class": DebertaModel, "config_class": DebertaConfig},
    "debertav2": {"model_class": DebertaV2Model, "config_class": DebertaV2Config},
    "distilbert": {"model_class": DistilBertModel, "config_class": DistilBertConfig},
    "dpr": {"model_class": DPRQuestionEncoder, "config_class": DPRConfig},
    "electra": {"model_class": ElectraModel, "config_class": ElectraConfig},
    "encdec": {
        "model_class": EncoderDecoderModel
    },  # EncoderDecoder models are more generic
    "ernie": {"model_class": ErnieModel, "config_class": ErnieConfig},
    "erniem": {"model_class": ErnieMModel, "config_class": ErnieMConfig},
    "esm": {"model_class": EsmModel, "config_class": EsmConfig},
    "falcon": {"model_class": FalconModel, "config_class": FalconConfig},
    "flaubert": {"model_class": FlaubertModel, "config_class": FlaubertConfig},
    "fnet": {"model_class": FNetModel, "config_class": FNetConfig},
    "fsmt": {"model_class": FSMTModel, "config_class": FSMTConfig},
    "gpt2": {"model_class": GPT2Model, "config_class": GPT2Config},
    "gptneo": {"model_class": GPTNeoModel, "config_class": GPTNeoConfig},
    "gptneox": {"model_class": GPTNeoXModel, "config_class": GPTNeoXConfig},
    "gptj": {"model_class": GPTJModel, "config_class": GPTJConfig},
    "llama": {"model_class": LlamaModel, "config_class": LlamaConfig},
    "longformer": {"model_class": LongformerModel, "config_class": LongformerConfig},
    "longt5": {"model_class": LongT5Model, "config_class": LongT5Config},
    "luke": {"model_class": LukeModel, "config_class": LukeConfig},
    "marianmt": {"model_class": MarianMTModel, "config_class": MarianConfig},
    "mbart": {"model_class": MBartModel, "config_class": MBartConfig},
    "megatronbert": {
        "model_class": MegatronBertModel,
        "config_class": MegatronBertConfig,
    },
    "mobilebert": {"model_class": MobileBertModel, "config_class": MobileBertConfig},
    "mpnet": {"model_class": MPNetModel, "config_class": MPNetConfig},
    "mt5": {"model_class": MT5Model, "config_class": MT5Config},
    "nezha": {"model_class": NezhaModel, "config_class": NezhaConfig},
    "nystromformer": {
        "model_class": NystromformerModel,
        "config_class": NystromformerConfig,
    },
    "opt": {"model_class": OPTModel, "config_class": OPTConfig},
    "pegasus": {"model_class": PegasusModel, "config_class": PegasusConfig},
    "plbart": {"model_class": PLBartModel, "config_class": PLBartConfig},
    "prophetnet": {"model_class": ProphetNetModel, "config_class": ProphetNetConfig},
    "qdqbert": {"model_class": QDQBertModel, "config_class": QDQBertConfig},
    "reformer": {"model_class": ReformerModel, "config_class": ReformerConfig},
    "rembert": {"model_class": RemBertModel, "config_class": RemBertConfig},
    "retrivbert": {"model_class": RetriBertModel, "config_class": RetriBertConfig},
    "roberta": {"model_class": RobertaModel, "config_class": RobertaConfig},
    "roformer": {"model_class": RoFormerModel, "config_class": RoFormerConfig},
    "squeezebert": {"model_class": SqueezeBertModel, "config_class": SqueezeBertConfig},
    "t5": {"model_class": T5Model, "config_class": T5Config},
    "xlm": {"model_class": XLMModel, "config_class": XLMConfig},
    "xlmroberta": {"model_class": XLMRobertaModel, "config_class": XLMRobertaConfig},
    "xlnet": {"model_class": XLNetModel, "config_class": XLNetConfig},
}


def load_model_from_huggingface(model_name, config_path):
    """
    Dynamically load a model and its configuration from HuggingFace's transformers library.

    Args:
        model_name (str): The name of the model, e.g., "bert" for BertModel.
        config_path (str): Path to the model configuration file (configs.json).

    Returns:
        model (nn.Module): Instantiated transformer model.
    """

    try:
        # Capitalize the first letter of model_name
        # model_class_name = f"{model_name.capitalize()}Model"
        # config_class_name = f"{model_name.capitalize()}Config"
        model_class = MODEL_CLASS_MAPPING[model_name.lower()]["model_class"]
        config_class = MODEL_CLASS_MAPPING[model_name.lower()]["config_class"]
        print(model_class)
        print(config_class)
        # transformers_module = importlib.import_module("transformers")
        # model_class = getattr(transformers_module, model_class_name)
        # config_class = getattr(transformers_module, config_class_name)

        # Load the configuration from the json file
        with open(config_path, "r") as f:
            config_dict = json.load(f)

        # Get the signature of the config class to know what arguments it accepts
        config_signature = inspect.signature(config_class)

        # Filter the config_dict to only include arguments accepted by the config class
        valid_config_params = {
            k: v for k, v in config_dict.items() if k in config_signature.parameters
        }

        # Initialize the configuration and model with valid parameters
        config = config_class(**valid_config_params)
        model = model_class(config)

        # logging.info(f"Loaded {model_class_name} with provided configurations.")
        return model

    except (ImportError, AttributeError) as e:
        raise ImportError(
            f"Model {model_name} is not available in HuggingFace transformers."
        )


def load_model_from_file(model_file, config_path):
    """Loads the user-defined model from a Python file."""
    spec = importlib.util.spec_from_file_location("user_defined_model", model_file)
    user_model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user_model)
    with open(config_path) as config_file:
        config_data = json.load(config_file)
    model_config = user_model.ModelConfig(
        **config_data
    )  # Assuming a defined ModelConfig
    model = user_model.Model(model_config)  # Assuming the user defines Model class
    return model
