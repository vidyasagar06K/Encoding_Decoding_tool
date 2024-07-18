import numpy as np
import matplotlib.pyplot as plt


def nrz_l_encode(data):
    encoded_data = []
    for bit in data:
        if bit == '1':
            encoded_data.append(1)
        else:
            encoded_data.append(0)
    return encoded_data


def nrz_i_encode(data):
    encoded_data = []
    previous_bit = 0
    for bit in data:
        if bit == '0':
            encoded_data.append(previous_bit)
        else:
            encoded_data.append(-previous_bit)
            previous_bit = int(bit)
    return encoded_data


def manchester_encode(data):
    encoded_data = []
    for bit in data:
        encoded_data.append(int(bit))
        encoded_data.append(1 - int(bit))
    return encoded_data


def differential_manchester_encode(data):
    encoded_data = []
    previous_bit = 1
    for bit in data:
        if bit == str(previous_bit):
            encoded_data.append(0)
        else:
            encoded_data.append(1)
            previous_bit = int(bit)
    return encoded_data


def ami_encode(data):
    encoded_data = []
    previous_bit = 1
    for bit in data:
        if bit == '0':
            encoded_data.append(-previous_bit)
        else:
            encoded_data.append(previous_bit)
            previous_bit = int(bit)
    return encoded_data


def b8zs_encode(data):
    encoded_data = []
    zero_count = 0
    for bit in data:
        if bit == '0':
            zero_count += 1
            if zero_count == 8:
                encoded_data.extend([0, 0, 0, 1, 1])
                zero_count = 0
        else:
            encoded_data.append(int(bit))
            zero_count = 0
    return encoded_data


def hdb3_encode(data):
    encoded_data = []
    zero_count = 0
    previous_bit = 0
    for bit in data:
        if bit == '0':
            zero_count += 1
            if zero_count == 4:
                if previous_bit == 0:
                    encoded_data.extend([0, 0, 0])
                else:
                    encoded_data.extend([0, 0, 1])
                zero_count = 0
        else:
            encoded_data.append(int(bit))
            previous_bit = int(bit)
            zero_count = 0
    return encoded_data


def pcm_encode(analog_signal):
    digital_signal = [int(sample * 255) for sample in analog_signal]
    return digital_signal


def dm_encode(analog_signal):
    digital_signal = []
    previous_sample = 0
    for sample in analog_signal:
        quantized_difference = sample - previous_sample
        if quantized_difference > 0:
            digital_signal.append(1)
        else:
            digital_signal.append(0)
        previous_sample = sample
    return digital_signal


def pcm_decode(encoded_data):
    analog_signal = [sample / 255.0 for sample in encoded_data]
    return analog_signal


def dm_decode(encoded_data):
    analog_signal = [0]
    for bit in encoded_data:
        if bit == 1:
            analog_signal.append(analog_signal[-1] + 1)
        else:
            analog_signal.append(analog_signal[-1] - 1)
    return analog_signal


def nrz_l_decode(encoded_data):
    decoded_data = ['1' if level == 1 else '0' for level in encoded_data]
    return decoded_data


def nrz_i_decode(encoded_data):
    decoded_data = []
    current_bit = 0
    for level in encoded_data:
        if level == 0:
            decoded_data.append(str(current_bit))
        else:
            current_bit = 1 - current_bit
            decoded_data.append(str(current_bit))
    return decoded_data


def manchester_decode(encoded_data):
    decoded_data = []
    for i in range(0, len(encoded_data), 2):
        decoded_data.append(str(encoded_data[i]))
    return decoded_data


def differential_manchester_decode(encoded_data):
    decoded_data = []
    current_bit = 0
    for i in range(0, len(encoded_data), 2):
        if encoded_data[i] == 1:
            current_bit = 1 - current_bit
        decoded_data.append(str(current_bit))
    return decoded_data


def ami_decode(encoded_data):
    decoded_data = []
    for level in encoded_data:
        if level == 0:
            decoded_data.append('0')
        else:
            decoded_data.append('1')
    return decoded_data


def b8zs_decode(encoded_data):
    decoded_data = []
    zero_count = 0
    for level in encoded_data:
        if level == 0:
            zero_count += 1
            if zero_count == 4:
                zero_count = 0
                continue
        else:
            zero_count = 0
        decoded_data.append(str(level))
    return decoded_data


def hdb3_decode(encoded_data):
    decoded_data = []
    zero_count = 0
    previous_bit = 0
    for level in encoded_data:
        if level == 0:
            zero_count += 1
            if zero_count == 4:
                if previous_bit == 0:
                    zero_count = 0
                    continue
                else:
                    decoded_data.extend(['0', '0', '0'])
                    zero_count = 0
        else:
            previous_bit = 1 - previous_bit
            zero_count = 0
            decoded_data.append(str(previous_bit))
    return decoded_data


def get_user_input():
    input_type = input("Enter input type (analog/digital): ").lower()

    if input_type == 'digital':
        digital_data = input("Enter digital data stream (e.g., 101001): ")
        return 'digital', digital_data
    elif input_type == 'analog':
        analog_data = [float(x) for x in input("Enter analog signal values separated by space: ").split()]
        return 'analog', analog_data
    else:
        print("Invalid input type. Please enter 'analog' or 'digital'.")
        return get_user_input()


def find_longest_palindrome(data):
    binary_data = ''.join(map(str, data))
    palindromes = [binary_data[i:j + 1] for i in range(len(binary_data)) for j in range(i, len(binary_data)) if
                   binary_data[i:j + 1] == binary_data[i:j + 1][::-1]]
    longest_palindrome = max(palindromes, key=len, default="")
    return longest_palindrome


def plot_digital_data(data, encoded_data, encoding_option):
    data = [int(bit) for bit in data]

    time_steps_data = np.arange(0, len(data) * 2, 2)
    time_steps_encoded = np.arange(1, len(encoded_data) * 2, 2)

    plt.figure(figsize=(10, 6))
    plt.step(time_steps_data, data, label='Digital Data', where='post', color='blue', marker='o', linestyle='--')
    plt.step(time_steps_encoded, encoded_data, label=f'{encoding_option} Encoding', where='mid', color='red',
             marker='o')

    plt.title(f'{encoding_option} Encoding of Digital Data')
    plt.xlabel('Time Steps')
    plt.ylabel('Digital Signal Level')
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    encoded_data = []
    try:
        input_type, data = get_user_input()

        if input_type == 'digital':
            longest_palindrome = find_longest_palindrome(data)
            print("Longest Palindrome:", longest_palindrome)

            encoding_option = input(
                "Choose line encoding scheme (NRZ-L, NRZ-I, Manchester, "
                "Differential Manchester, AMI, B8ZS, HDB3): "
            ).upper()

            if encoding_option == 'AMI':
                scrambling_option = input("Do you want scrambling for AMI? (yes/no): ").lower()
                if scrambling_option == 'yes':
                    scrambling_type = input("Choose scrambling type (B8ZS, HDB3): ").upper()
                    encoded_data = b8zs_encode(data) if scrambling_type == 'B8ZS' else hdb3_encode(data)
                else:
                    encoded_data = ami_encode(data)
            else:
                encoding_functions = {
                    'NRZ-L': nrz_l_encode,
                    'NRZ-I': nrz_i_encode,
                    'MANCHESTER': manchester_encode,
                    'DIFFERENTIAL MANCHESTER': differential_manchester_encode,
                    'B8ZS': b8zs_encode,
                    'HDB3': hdb3_encode
                }
                if encoding_option not in encoding_functions:
                    raise ValueError("Invalid encoding option. Please choose a valid option.")

                encoded_data = encoding_functions.get(encoding_option, lambda x: None)(data)
            plot_digital_data(data, encoded_data, encoding_option)

            decode_option = input("Do you want to decode the signal? (yes/no): ").lower()

            if decode_option == 'yes':
                decoding_functions = {
                    'NRZ-L': nrz_l_decode,
                    'NRZ-I': nrz_i_decode,
                    'MANCHESTER': manchester_decode,
                    'DIFFERENTIAL MANCHESTER': differential_manchester_decode,
                    'B8ZS': b8zs_decode,
                    'HDB3': hdb3_decode,
                    'AMI': ami_decode
                }
                if encoding_option not in decoding_functions:
                    raise ValueError("Invalid decoding option. Please choose a valid option.")

                decoded_data = decoding_functions.get(encoding_option, lambda x: None)(encoded_data)
                print("Decoded Digital Stream:", ''.join(decoded_data))

        elif input_type == 'analog':
            modulation_option = input("Choose modulation scheme (PCM/DM): ").upper()

            if modulation_option == 'PCM':
                encoded_data = pcm_encode(data)
            elif modulation_option == 'DM':
                encoded_data = dm_encode(data)
            else:
                raise ValueError("Invalid modulation scheme. Please enter 'PCM' or 'DM'.")

            decode_option = input("Do you want to decode the signal? (yes/no): ").lower()

            if decode_option == 'yes':
                decoding_functions_analog = {
                    'PCM': pcm_decode,
                    'DM': dm_decode
                }
                if modulation_option not in decoding_functions_analog:
                    raise ValueError("Invalid decoding option. Please choose a valid option.")

                decoded_analog_data = decoding_functions_analog.get(modulation_option, lambda x: None)(encoded_data)
                print("Decoded Analog Signal:", decoded_analog_data)

    except ValueError as e:
        print(f"Error: {e}")

    print("Digital Signal Produced:", encoded_data)


if __name__ == "__main__":
    main()
