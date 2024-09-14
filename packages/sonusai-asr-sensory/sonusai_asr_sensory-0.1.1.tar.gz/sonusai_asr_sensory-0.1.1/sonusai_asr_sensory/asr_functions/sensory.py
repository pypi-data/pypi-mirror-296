from sonusai.mixture import AudioT
from sonusai.utils import ASRResult


def sensory(audio: AudioT, **config) -> ASRResult:
    import pickle
    import shutil
    import string
    import subprocess
    from pathlib import Path
    from timeit import default_timer as timer

    from sonusai import SonusAIError
    from sonusai.utils import ASRResult
    from sonusai.utils import float_to_int16

    model_name = config.get('model', 'stt-enUS-automotive-small_medium-2.0.8-BBB-ff.snsr')

    snsr_exec_name = 'snsr-eval'

    snsr_exec = shutil.which(snsr_exec_name)
    if snsr_exec is None:
        raise FileNotFoundError(f'{snsr_exec_name} not found')

    snsr_root = Path(Path(Path(snsr_exec).parent).parent)
    snsr_model = snsr_root / 'model' / model_name

    command = f'{snsr_exec}'
    command += f' -t {snsr_model}'
    command += f' -'

    s_time = timer()
    result = subprocess.run([command],
                            input=pickle.dumps(float_to_int16(audio)),
                            shell=True,
                            capture_output=True)
    e_time = timer()
    elapsed = e_time - s_time
    if result.stderr:
        raise SonusAIError(result.stderr.decode('utf-8'))

    text = ' '.join(result.stdout.decode('utf-8').splitlines()[-1].strip().split()[2:])
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    return ASRResult(text=text, asr_cpu_time=elapsed)


"""
Sensory results:
P     80    400 the birch
P     80    920 the birch canoe s
P     80   1760 the birch canoe slid on the smoke
P     40   2280 the birch canoe slid on the smooth plan
NLU intent: no_command (0.9991) = the birch canoe slid on the smooth planks
    40   2560 the birch canoe slid on the smooth planks
"""
