from sonusai.mixture.datatypes import AudioStatsMetrics
from sonusai.mixture.datatypes import AudioT


def calc_audio_stats(audio: AudioT, win_len: float = None) -> AudioStatsMetrics:
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.mixture import Transformer

    args = ['stats']
    if win_len is not None:
        args.extend(['-w', str(win_len)])

    tfm = Transformer()

    _, _, out = tfm.build(input_array=audio,
                          sample_rate_in=SAMPLE_RATE,
                          output_filepath='-n',
                          extra_args=args,
                          return_output=True)

    stats = {}
    lines = out.split('\n')
    for line in lines:
        split_line = line.split()
        if len(split_line) == 0:
            continue
        value = split_line[-1]
        key = ' '.join(split_line[:-1])
        stats[key] = value

    return AudioStatsMetrics(
        dco=float(stats['DC offset']),
        min=float(stats['Min level']),
        max=float(stats['Max level']),
        pkdb=float(stats['Pk lev dB']),
        lrms=float(stats['RMS lev dB']),
        pkr=float(stats['RMS Pk dB']),
        tr=float(stats['RMS Tr dB']),
        cr=float(stats['Crest factor']),
        fl=float(stats['Flat factor']),
        pkc=int(stats['Pk count']),
    )
