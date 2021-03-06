#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Sat Nov  7 02:37:58 2015
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
        self.audio_rate = audio_rate = int(48e3)
        self.rtl_rate = rtl_rate = int(240e3)
        self.out_intermediary_rate = out_intermediary_rate = audio_rate*4
        self.out_gain = out_gain = .25
        self.out_frequency_offset = out_frequency_offset = -50e3
        self.out_frequency = out_frequency = 145.521e6
        self.out_audio_inverted = out_audio_inverted = True
        self.in_frequency_offset = in_frequency_offset = 0
        self.in_frequency = in_frequency = 145.551e6
        self.in_final_gain = in_final_gain = 0.5
        self.in_decimation_factor = in_decimation_factor = 8
        self.in_audio_inverted = in_audio_inverted = True
        self.hackrf_rate = hackrf_rate = 2e6
        self.dstar_bandwidth = dstar_bandwidth = 6.5e3

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
        self.osmosdr_sink_0.set_if_gain(0, 0)
        self.osmosdr_sink_0.set_bb_gain(0, 0)
        self.osmosdr_sink_0.set_antenna("0", 0)
        self.osmosdr_sink_0.set_bandwidth(100e3, 0)
          
        self.low_pass_filter_1 = filter.fir_filter_ccf(5, firdes.low_pass(
        	1, rtl_rate, dstar_bandwidth*2, 500, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, audio_rate, dstar_bandwidth*2, 200, firdes.WIN_KAISER, 6.76))
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(1, (1, ), 0-out_frequency_offset, out_intermediary_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(128, True)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_vff(((-1 if out_audio_inverted else 1)*out_gain, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((0-in_final_gain if in_audio_inverted else in_final_gain, ))
        self.audio_source_0 = audio.source(audio_rate, "hw:10,1", True)
        self.audio_sink_1 = audio.sink(audio_rate, "plughw:11,0", True)
        self.analog_pwr_squelch_xx_1 = analog.pwr_squelch_cc(-30, 1, 1, False)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_ff(-60, 1, 1, True)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=int(audio_rate),
        	quad_rate=int(out_intermediary_rate),
        	tau=0,
        	max_dev=dstar_bandwidth,
        )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=audio_rate,
        	quad_rate=audio_rate,
        	tau=0.000000000000000000001,
        	max_dev=dstar_bandwidth*2,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.analog_nbfm_tx_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))    
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.blocks_multiply_const_vxx_2, 0))    
        self.connect((self.analog_pwr_squelch_xx_1, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.audio_source_0, 0), (self.dc_blocker_xx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.analog_pwr_squelch_xx_0, 0))    
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.rational_resampler_xxx_3, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_nbfm_tx_0, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.analog_pwr_squelch_xx_1, 0))    
        self.connect((self.rational_resampler_xxx_3, 0), (self.osmosdr_sink_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_1, 0))    


    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.set_out_intermediary_rate(self.audio_rate*4)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.audio_rate, self.dstar_bandwidth*2, 200, firdes.WIN_KAISER, 6.76))

    def get_rtl_rate(self):
        return self.rtl_rate

    def set_rtl_rate(self, rtl_rate):
        self.rtl_rate = rtl_rate
        self.rtlsdr_source_0.set_sample_rate(self.rtl_rate)
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.rtl_rate, self.dstar_bandwidth*2, 500, firdes.WIN_HAMMING, 6.76))

    def get_out_intermediary_rate(self):
        return self.out_intermediary_rate

    def set_out_intermediary_rate(self, out_intermediary_rate):
        self.out_intermediary_rate = out_intermediary_rate

    def get_out_gain(self):
        return self.out_gain

    def set_out_gain(self, out_gain):
        self.out_gain = out_gain
        self.blocks_multiply_const_vxx_2.set_k(((-1 if self.out_audio_inverted else 1)*self.out_gain, ))

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

    def get_out_audio_inverted(self):
        return self.out_audio_inverted

    def set_out_audio_inverted(self, out_audio_inverted):
        self.out_audio_inverted = out_audio_inverted
        self.blocks_multiply_const_vxx_2.set_k(((-1 if self.out_audio_inverted else 1)*self.out_gain, ))

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

    def get_in_decimation_factor(self):
        return self.in_decimation_factor

    def set_in_decimation_factor(self, in_decimation_factor):
        self.in_decimation_factor = in_decimation_factor

    def get_in_audio_inverted(self):
        return self.in_audio_inverted

    def set_in_audio_inverted(self, in_audio_inverted):
        self.in_audio_inverted = in_audio_inverted
        self.blocks_multiply_const_vxx_1.set_k((0-self.in_final_gain if self.in_audio_inverted else self.in_final_gain, ))

    def get_hackrf_rate(self):
        return self.hackrf_rate

    def set_hackrf_rate(self, hackrf_rate):
        self.hackrf_rate = hackrf_rate
        self.osmosdr_sink_0.set_sample_rate(self.hackrf_rate)

    def get_dstar_bandwidth(self):
        return self.dstar_bandwidth

    def set_dstar_bandwidth(self, dstar_bandwidth):
        self.dstar_bandwidth = dstar_bandwidth
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.audio_rate, self.dstar_bandwidth*2, 200, firdes.WIN_KAISER, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.rtl_rate, self.dstar_bandwidth*2, 500, firdes.WIN_HAMMING, 6.76))


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.start()
    tb.wait()
