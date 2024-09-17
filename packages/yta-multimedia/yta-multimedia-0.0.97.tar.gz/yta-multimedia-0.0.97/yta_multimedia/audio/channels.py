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


#       8D Effect
# Thanks to: https://github.com/dashroshan/8d-slow-reverb
pan_jump_percentage = 5  # Percentage of dist b/w L-R to jump at a time
PAN_BOUNDARY = 100  # Perctange of dist from center that audio source can go
volume_multiplier = 6  # Max volume DB increase at edges

def pan_array(time_from_left_to_right: int = 10000):
    """
    Generates an array of range -1.0 to 1.0 which control the position 
    of audio source (pan effect). -1.0 places the audio source on 
    extreme left, 0.0 on center, and 1.0 on extreme right. The audio is 
    splitted into multiple pieces and each piece is played from a
    position decided by this array.

    Returns pan position array along with the time length of each piece 
    to play at one position.
    """
    # Total pieces when audio source is moving
    pieces_center_to_right = PAN_BOUNDARY / pan_jump_percentage
    pieces_left_to_right = pieces_center_to_right * 2
    # Time length of each piece
    piece_time = int(time_from_left_to_right / pieces_left_to_right)

    pan = []
    left = -PAN_BOUNDARY  # Audio source to start from extreme left

    while left <= PAN_BOUNDARY:  # Until audio source position reaches extreme right
        pan.append(left)  # Append the position to pan array
        left += pan_jump_percentage  # Increment to next position

    # [-100, -95, -90, ..., -5, 0, 5]

    # Above loop generates number in range -100 to 100, this converts it to -1.0 to 1.0 scale
    pan = [x / 100 for x in pan]

    return pan, piece_time

def effect_8d(audio):
    """
    Generates a 8d sound effect by splitting the 'audio'' into multiple 
    smaller pieces, pans each piece to make the sound source seem like 
    it is moving from L to R and R to L in loop, decreases volume towards
    center position to make the movement sound like it is a circle 
    instead of straight line.
    """
    audio = audio_to_audiosegment(audio)
    # TODO: 'audio' was AudioSegment.from_file()

    # Get the pan position array and time length of each piece to play at one position
    pan, piece_time = pan_array()

    sound8d = audio[0]  # Stores the 8d sound
    pan_index = 0  # Index of current pan position of pan array

    # We loop through the pan array forward once, and then in reverse (L to R, then R to L)
    iterate_pan_array_forward = True

    # Loop through starting time of each piece
    for time in range(0, len(audio) - piece_time, piece_time):
        # time + piece_time = ending time of piece
        piece = audio[time: time + piece_time]

        # If at first element of pan array (Left) then iterate forward
        if pan_index == 0:
            iterate_pan_array_forward = True

        # If at last element of pan array (Right) then iterate backward
        if pan_index == len(pan) - 1:
            iterate_pan_array_forward = False

        # (pan_boundary / 100) brings pan_boundary to the same scale as elements
        # of pan array i.e. -1.0 to 1.0
        # abs(pan[pan_index]) / (panBoundary / 100) = 1 for extreme left/right and 0 for center
        # abs(pan[pan_index]) / (panBoundary / 100) * volumeMultiplier = volumeMultiplier for extreme left/right and 0 for center
        # Hence, vol_adjust = 0 for extreme left/right and volumeMultiplier for center
        vol_adjust = volume_multiplier - (
            abs(pan[pan_index]) / (PAN_BOUNDARY / 100) * volume_multiplier
        )

        # Decrease piece volume by vol_adjust i.e. max volume at extreme 
        # left/right and decreases towards center
        piece -= vol_adjust

        # Pan the piece of sound according to the pan array element
        pannedPiece = piece.pan(pan[pan_index])

        # Iterates the pan array from left to right, then right to left,
        # then left to right and so on..
        if iterate_pan_array_forward:
            pan_index += 1
        else:
            pan_index -= 1

        # Add this panned piece of sound with adjusted volume to the 8d sound
        sound8d = sound8d + pannedPiece

    return sound8d

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
    AUDIO_PART_TIME = audio.duration_seconds / NUM_OF_PARTS

    cont = 0
    while ((cont * AUDIO_PART_TIME) < (audio.duration_seconds)):
        coordinate = cont * AUDIO_PART_SCREEN_SIZE
        print(coordinate)
        audio = adjust_audio_channels(audio, x_coordinate_to_channel_pan(coordinate), cont * AUDIO_PART_TIME, (cont + 1) * AUDIO_PART_TIME)
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
    if not x:
        raise Exception('No "x" provided.')
    
    if x < 0 or x > 1919:
        raise Exception('The parameter "x" must be a valid number between 0 and 1919.')

    return -1.0 + (x * 2.0 / 1919)

def adjust_audio_channels(audio, channel_pan: float = 0.0, start_time = None, end_time = None):
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
    """
    audio = audio_to_audiosegment(audio)

    if not channel_pan:
        raise Exception('No "channel_pan" provided.')

    if channel_pan < -1.0 or channel_pan > 1.0:
        raise Exception('The "channel_pan" parameter must be a value between -1.0 and 1.0.')
    
    if not start_time:
        start_time = 0

    if not end_time:
        end_time = audio.duration_seconds

    if start_time < 0:
        raise Exception('The "start_time" parameter cannot be lower than 0.')
    
    if start_time > audio.duration_seconds:
        raise Exception('The "start_time" cannot be greater than the actual "audio" duration.')
    
    if start_time > end_time:
        raise Exception('The "start_time" cannot be greater than the "end_time".')
    
    if end_time < 0:
        raise Exception('The "start_time" parameter cannot be lower than 0.')
    
    if end_time > audio.duration_seconds:
        raise Exception('The "end_time" cannot be greater than the actual "audio" duration.')
    
    if channel_pan < -1.0 or channel_pan > 1.0:
        raise Exception('The "channel_pan" parameter must be between -1.0 (left) and 1.0 (right)')

    audio = audio[start_time: end_time].pan(channel_pan)

    return audio