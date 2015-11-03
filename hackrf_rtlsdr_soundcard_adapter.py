#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Mon Nov  2 22:27:37 2015
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time

class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.audio_rate = audio_rate = int(48e3)
        self.soundcard_is_inverted = soundcard_is_inverted = False
        self.out_intermediary_rate = out_intermediary_rate = audio_rate*4
        self.out_frequency_offset = out_frequency_offset = -35e3
        self.out_frequency = out_frequency = 145.521e6
        self.hackrf_rate = hackrf_rate = 2e6
        self.dstar_bandwidth = dstar_bandwidth = 6.5e3

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_3 = filter.rational_resampler_ccc(
                interpolation=int(hackrf_rate),
                decimation=out_intermediary_rate,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_sink_0.set_sample_rate(hackrf_rate)
        self.osmosdr_sink_0.set_center_freq(out_frequency-out_frequency_offset, 0)
        self.osmosdr_sink_0.set_freq_corr(4, 0)
        self.osmosdr_sink_0.set_gain(14, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(100e3, 0)
          
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(1, (1, ), 0-out_frequency_offset, out_intermediary_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self.audio_source_0 = audio.source(audio_rate, "hw:10,1", True)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_ff(-80, 1, 1, True)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=int(audio_rate),
        	quad_rate=int(out_intermediary_rate),
        	tau=0,
        	max_dev=6.25e3*2,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_tx_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))    
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.analog_nbfm_tx_0, 0))    
        self.connect((self.audio_source_0, 0), (self.analog_pwr_squelch_xx_0, 0))    
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.rational_resampler_xxx_3, 0))    
        self.connect((self.rational_resampler_xxx_3, 0), (self.osmosdr_sink_0, 0))    


    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.set_out_intermediary_rate(self.audio_rate*4)

    def get_soundcard_is_inverted(self):
        return self.soundcard_is_inverted

    def set_soundcard_is_inverted(self, soundcard_is_inverted):
        self.soundcard_is_inverted = soundcard_is_inverted

    def get_out_intermediary_rate(self):
        return self.out_intermediary_rate

    def set_out_intermediary_rate(self, out_intermediary_rate):
        self.out_intermediary_rate = out_intermediary_rate

    def get_out_frequency_offset(self):
        return self.out_frequency_offset

    def set_out_frequency_offset(self, out_frequency_offset):
        self.out_frequency_offset = out_frequency_offset
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(0-self.out_frequency_offset)
        self.osmosdr_sink_0.set_center_freq(self.out_frequency-self.out_frequency_offset, 0)

    def get_out_frequency(self):
        return self.out_frequency

    def set_out_frequency(self, out_frequency):
        self.out_frequency = out_frequency
        self.osmosdr_sink_0.set_center_freq(self.out_frequency-self.out_frequency_offset, 0)

    def get_hackrf_rate(self):
        return self.hackrf_rate

    def set_hackrf_rate(self, hackrf_rate):
        self.hackrf_rate = hackrf_rate
        self.osmosdr_sink_0.set_sample_rate(self.hackrf_rate)

    def get_dstar_bandwidth(self):
        return self.dstar_bandwidth

    def set_dstar_bandwidth(self, dstar_bandwidth):
        self.dstar_bandwidth = dstar_bandwidth


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()
