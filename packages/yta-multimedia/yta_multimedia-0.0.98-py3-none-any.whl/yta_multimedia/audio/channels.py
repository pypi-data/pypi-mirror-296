from yta_general_utils.file_processor import file_is_audio_file, get_file_extension
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
from enum import Enum

import numpy as np
import io
import scipy.io.wavfile as wavfile
from typing import Union

# TODO: Move to a utils
def audio_to_audiosegment(audio):
    """
    Forces the provided 'audio' to be a pydub AudioSegment
    and returns it if valid'audio' provided or raises an
    Exception if not.
    """
    if not audio:
        raise Exception('No "audio" provided.')
    
    if isinstance(audio, str):
        if not file_is_audio_file(audio):
            raise Exception('Provided "audio" filename is not a valid audio file.')
        
        audio = AudioSegment.from_file(audio)
    elif isinstance(audio, np.ndarray):
        # TODO: Check this works
        audio = numpy_to_audiosegment(audio)
    elif isinstance(audio, AudioSegment):
        pass
    elif isinstance(audio, AudioFileClip):
        # TODO: Check this works
        audio = audiofileclip_to_numpy(audio)

    return audio

# TODO: Move to a utils
def numpy_to_audiosegment(audio, sample_rate):
    """
    Convers the provided 'audio' numpy array, that contains the audio data
    and must be in float32 or int16, to a pydub AudioSegment.
    """
    # Normalize audio_array if it's not already in int16 format
    if audio.dtype != np.int16:
        if audio.dtype != np.float32:
            raise Exception('Provided "audio" is not np.int16 nor np.float32.')
        
        # Assuming the audio_array is in float32 with values between -1 and 1
        audio = (audio * 32767).astype(np.int16)
    
    # Create a BytesIO object
    with io.BytesIO() as buffer:
        wavfile.write(buffer, sample_rate, audio)
        buffer.seek(0)
        
        audio_segment = AudioSegment.from_file(buffer, format = 'wav')
    
    return audio_segment

# TODO: Move to a utils
def audiofileclip_to_numpy(audio: AudioFileClip):
    """
    Convers the provided 'audio' moviepy AudioFileClip to a numpy
    array that will be np.float32.
    """
    if not audio:
        raise Exception('No "audio" provided.')
    
    if not isinstance(audio, AudioFileClip):
        raise Exception('The "audio" provided is not a moviepy AudioFileClip.')
    
    # Extract the audio samples as a numpy array
    audio_array = audio.to_soundarray(fps = audio.fps)
    
    # If the audio is stereo, the array will have shape (n_samples, 2)
    # Convert to float32 if needed, to handle audio samples as floats
    if audio_array.dtype != np.float32:
        audio_array = audio_array.astype(np.float32)
    
    # Normalize if the data is not already normalized
    if np.max(np.abs(audio_array)) > 1.0:
        audio_array /= np.max(np.abs(audio_array))
    
    return audio_array

class AudioChannel(Enum):
    LEFT = 1
    RIGHT = 0

def isolate_channel(audio, channel: AudioChannel = AudioChannel.LEFT, output_filename: Union[str, None] = None):
    """
    Processes the given 'audio' (if valid) and extracts the requested
    'channel' only by isolating it, that will be returned as a pydub 
    AudioSegment.
    """
    audio = audio_to_audiosegment(audio)

    if not channel:
        raise Exception('No "channel" provided.')
    
    if not isinstance(channel, AudioChannel):
        raise Exception('Provided "channel" is not an AudioChannel.')
    
    # Numpy to be able to work
    samples = np.array(audio.get_array_of_samples())
    channels = audio.channels
    
    if channels == 1:
        # TODO: Audio is mono, make it have 2 channels and only left filled
        return audio
    
    # Reshape the samples array to separate left and right channels
    samples = samples.reshape(-1, 2)
    
    # Set the right channel samples to zero
    samples[:, channel.value] = 0
    
    # Flatten the array back to the original format
    new_samples = samples.flatten()
    
    # Convert the numpy array back to AudioSegment
    new_audio_segment = audio._spawn(new_samples.astype(np.int16).tobytes())

    if output_filename:
        extension = get_file_extension(output_filename)
        # TODO: Create filename validator to validate if filename is video,
        # audio, etc.
        if not extension:
            output_filename += '.wav'
            extension = '.wav'

        new_audio_segment.export(out_f = output_filename, format = extension)
    
    return new_audio_segment


def custom_8d_effect(audio):
    """
    Generates a 8d sound effect by splitting the 'audio'' into multiple 
    smaller pieces, pans each piece to make the sound source seem like 
    it is moving from L to R and R to L in loop, decreases volume towards
    center position to make the movement sound like it is a circle 
    instead of straight line.
    """
    audio = audio_to_audiosegment(audio)

    SCREEN_SIZE = 1920
    NUM_OF_PARTS = 80
    AUDIO_PART_SCREEN_SIZE = SCREEN_SIZE / NUM_OF_PARTS
    AUDIO_PART_TIME = audio.duration_seconds * 1000 / NUM_OF_PARTS

    cont = 0
    while ((cont * AUDIO_PART_TIME) < audio.duration_seconds * 1000):
        coordinate = cont * AUDIO_PART_SCREEN_SIZE
        channel_pan = x_coordinate_to_channel_pan(coordinate)
        volume_adjustment = 5 - (abs(channel_pan) / NUM_OF_PARTS) * 5

        start_time = cont * AUDIO_PART_TIME
        end_time = (cont + 1) * AUDIO_PART_TIME
        # I do this because of a small error that makes it fail
        if end_time > audio.duration_seconds * 1000:
            end_time = audio.duration_seconds * 1000
        audio = adjust_audio_channels(audio, channel_pan, volume_adjustment, start_time, end_time)
        cont += 1

    return audio

def x_coordinate_to_channel_pan(x: int):
    """
    This method calculates the corresponding channel pan value (between -1.0 and
    1.0) for the provided "x" coordinate (in an hypotetic scene of 1920x1080).
    This means that an "x" of 0 will generate a -1.0 value, and an "x" of 1919
    will generate a 1.0 value.

    This method has been created to be usede in transition effects sounds, to be
    dynamically panned to fit the element screen position during the movement.
    """
    if not x and x != 0:
        raise Exception('No "x" provided.')
    
    if x < 0 or x > 1919:
        raise Exception('The parameter "x" must be a valid number between 0 and 1919.')

    return -1.0 + (x * 2.0 / 1919)

def adjust_audio_channels(audio, channel_pan: float = 0.0, volume_adjustment: float = 0.0, start_time = None, end_time = None):
    """
    This method allows you to set the amount of 'audio' you want to be
    sounding on each of the 2 channels (speakers), right and left. The
    'channel_pan' parameter must be a value between -1.0, which means
    left channel, and 1.0, that means right channel. A value of 0 means
    that the sound will sound equally in left and right channel. A value
    of 0.5 means that it will sound 25% in left channel and 75% in right
    channel.

    This method will apply the provided 'channel_pan' to the also provided
    'audio'. The 'start_time' and 'end_time' parameters determine the part
    of the audio you want the channel panning to be applied, and it is in
    seconds.

    TODO: Explain 'volume_adjustment' or remove it
    """
    audio = audio_to_audiosegment(audio)

    if not channel_pan:
        raise Exception('No "channel_pan" provided.')

    if channel_pan < -1.0 or channel_pan > 1.0:
        raise Exception('The "channel_pan" parameter must be a value between -1.0 and 1.0.')
    
    if not start_time:
        start_time = 0

    if not end_time:
        end_time = audio.duration_seconds * 1000

    if start_time < 0:
        raise Exception('The "start_time" parameter cannot be lower than 0.')
    
    if start_time > audio.duration_seconds * 1000:
        raise Exception('The "start_time" cannot be greater than the actual "audio" duration.')
    
    if start_time > end_time:
        raise Exception('The "start_time" cannot be greater than the "end_time".')
    
    if end_time < 0:
        raise Exception('The "start_time" parameter cannot be lower than 0.')
    
    if end_time > audio.duration_seconds * 1000:
        raise Exception('The "end_time" cannot be greater than the actual "audio" duration.')
    
    if channel_pan < -1.0 or channel_pan > 1.0:
        raise Exception('The "channel_pan" parameter must be between -1.0 (left) and 1.0 (right)')

    # Process the part we want
    modified_part = audio[start_time: end_time]
    # TODO: I think this is not necessary, maybe remove it (?)
    #modified_part -= volume_adjustment
    modified_part = modified_part.pan(channel_pan)

    if start_time == 0 and end_time == audio.duration_seconds * 1000:
        audio = modified_part
    elif start_time == 0:
        audio = modified_part + audio[end_time: audio.duration_seconds * 1000]
    elif end_time == audio.duration_seconds * 1000:
        audio = audio[0: start_time] + modified_part
    else:
        audio = audio[0: start_time] + modified_part + audio[end_time: audio.duration_seconds * 1000]

    return audio