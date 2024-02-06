#include <driver/i2s.h>

#define I2S_WS 25
#define I2S_SD 33
#define I2S_SCK 32
#define SAMPLE_BUFFER_SIZE 512  // Corrected declaration
#define SAMPLE_RATE 25000
// don't mess around with this
i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = (i2s_bits_per_sample_t)16,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = i2s_comm_format_t(I2S_COMM_FORMAT_STAND_I2S),
    .intr_alloc_flags = 0,
    .dma_buf_count = 8,
    .dma_buf_len = 512,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = -1
};

// and don't mess around with this
i2s_pin_config_t i2s_mic_pins = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = -1,
    .data_in_num = I2S_SD
};

void setup()
{
  // we need serial output for the plotter
  Serial.begin(500000);
  // start up the I2S peripheral
  i2s_driver_install(I2S_NUM_1, &i2s_config, 0, NULL);  // Corrected port number
  i2s_set_pin(I2S_NUM_1, &i2s_mic_pins);
}

int16_t raw_samples[SAMPLE_BUFFER_SIZE];
void loop() {
  // read from the I2S device
  size_t bytes_read = 0;
  i2s_read(I2S_NUM_1, raw_samples, sizeof(int16_t) * SAMPLE_BUFFER_SIZE, &bytes_read, portMAX_DELAY);

  // Send data over serial
  Serial.write((const char*)raw_samples, bytes_read);
}