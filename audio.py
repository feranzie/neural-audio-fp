from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile

aud=[
    "1066_SOGNO.wav",
    "1875_SOSPESI.wav",
    "20545_SOGNO.wav",
    "2332_SOGNO.wav",
    "30531_SOGNO.wav",
    "32794_ADRENALIN_PULSE.wav",
    "3306_SIGLA_RAI_3.wav",
    "3343_SIGLA_RAI_1.wav",
    "3354_IDENTITY_RAI_1.wav",
    "42398_BELIEVE.wav",
    "49136_LUMOS.wav",
    "49486_SOGNO.wav",
    "61994_SOSPESI.wav",
    "72741_OUTCONC_18_NEW.wav",
    "7328_SOSPESI.wav",
    "73561_RAI_UNO_REBRAND.wav",
    "74537_AFTERMATH_REPORT.wav",
    "74669_FANT_18_PIN.wav",
    "74672_TRIELLO_18_PIN.wav",
    "76372_PAROLONE_NEW.wav",
    "80154_PLATFORM.wav",
    "80583_SIGLA_RAI_3.wav",
    "80584_SIGLA_RAI_1.wav",
    "80588_SIGLA_RAI_3.wav",
    "81096_STK_CHI_COME_COSA_PIN.wav",
    "82021_SIGLA_TG1.wav",
    "85043_SOGNO.wav",
    "85351_PUNTADITO_PIN.wav",
    "86226_DADONE_PIN.wav",
    "86611_VOLTAPAGINA_PAROLONE_PIN.wav",
    "86662_DOPO_OFFERTA_1.wav",
    "86664_DOPO_OFFERTA_3.wav",
    "86665_DOVE_VUOI_ANDARE.wav",
    "86672_PACCHI_FORTUNATI.wav",
    "86674_QUATTRO_PACCHI.wav",
    "86678_SENSAZIONI.wav",
    "86680_TICCHETTIO.wav",
    
]
# Load the audio file
for i in aud:
    audio = AudioSegment.from_file(i)

    # Convert to mono (single channel)
    audio = audio.set_channels(1)

    # Resample the audio to 8000 Hz
    audio = audio.set_frame_rate(8000)

    # Export the resampled and mono audio
    resampled_audio_path = f"./prod/{i}"
    audio.export(resampled_audio_path, format="wav")

    # Read the resampled audio data
    sample_rate, data = wavfile.read(resampled_audio_path)

    # Check if the audio data needs to be trimmed or padded
    target_length = 8000  # example target length
    if data.shape[0] > target_length:
        data = data[:target_length]
    elif data.shape[0] < target_length:
        # Pad with zeros if the data is shorter than the target length
        padding = target_length - data.shape[0]
        data = np.pad(data, (0, padding), 'constant')

    # Now data is reshaped to the expected shape (8000,)
    print(data.shape)
