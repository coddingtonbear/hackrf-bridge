#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Nov  5 15:10:10 2015
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
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
        self.rtl_rate = rtl_rate = int(230400)
        self.in_frequency_offset = in_frequency_offset = 0
        self.in_frequency = in_frequency = 145.551e6
        self.in_final_gain = in_final_gain = 5
        self.in_audio_inverted = in_audio_inverted = True
        self.dstar_bandwidth = dstar_bandwidth = 6.5e3
        self.audio_rate = audio_rate = int(48e3)

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(rtl_rate)
        self.rtlsdr_source_0.set_center_freq(in_frequency+in_frequency_offset, 0)
        self.rtlsdr_source_0.set_freq_corr(69, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=audio_rate*3,
                decimation=rtl_rate,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_1 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, audio_rate*3, dstar_bandwidth*2, 200, firdes.WIN_HAMMING, 6.76))
        self.blocks_wavfile_sink_1 = blocks.wavfile_sink("/tmp/dstar_actual_output.wav", 1, audio_rate, 8)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((0-in_final_gain if in_audio_inverted else in_final_gain, ))
        self.audio_source_1 = audio.source(audio_rate, "hw:11,1", True)
        self.audio_sink_1 = audio.sink(audio_rate, "hw:11,0", False)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=audio_rate*3,
        	audio_decim=3,
        	deviation=dstar_bandwidth*2,
        	audio_pass=dstar_bandwidth*2,
        	audio_stop=dstar_bandwidth*3,
        	gain=1,
        	tau=0,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.audio_source_1, 0), (self.blocks_wavfile_sink_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_1, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.analog_fm_demod_cf_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.rational_resampler_xxx_1, 0))    


    def get_rtl_rate(self):
        return self.rtl_rate

    def set_rtl_rate(self, rtl_rate):
        self.rtl_rate = rtl_rate
        self.rtlsdr_source_0.set_sample_rate(self.rtl_rate)

    def get_in_frequency_offset(self):
        return self.in_frequency_offset

    def set_in_frequency_offset(self, in_frequency_offset):
        self.in_frequency_offset = in_frequency_offset
        self.rtlsdr_source_0.set_center_freq(self.in_frequency+self.in_frequency_offset, 0)

    def get_in_frequency(self):
        return self.in_frequency

    def set_in_frequency(self, in_frequency):
        self.in_frequency = in_frequency
        self.rtlsdr_source_0.set_center_freq(self.in_frequency+self.in_frequency_offset, 0)

    def get_in_final_gain(self):
        return self.in_final_gain

    def set_in_final_gain(self, in_final_gain):
        self.in_final_gain = in_final_gain
        self.blocks_multiply_const_vxx_1.set_k((0-self.in_final_gain if self.in_audio_inverted else self.in_final_gain, ))

    def get_in_audio_inverted(self):
        return self.in_audio_inverted

    def set_in_audio_inverted(self, in_audio_inverted):
        self.in_audio_inverted = in_audio_inverted
        self.blocks_multiply_const_vxx_1.set_k((0-self.in_final_gain if self.in_audio_inverted else self.in_final_gain, ))

    def get_dstar_bandwidth(self):
        return self.dstar_bandwidth

    def set_dstar_bandwidth(self, dstar_bandwidth):
        self.dstar_bandwidth = dstar_bandwidth
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.audio_rate*3, self.dstar_bandwidth*2, 200, firdes.WIN_HAMMING, 6.76))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.audio_rate*3, self.dstar_bandwidth*2, 200, firdes.WIN_HAMMING, 6.76))


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
