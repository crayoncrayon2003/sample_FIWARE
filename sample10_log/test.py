import os
import glob

ROOT   = os.path.dirname(os.path.abspath(__file__))
LOGDIR = os.path.join(ROOT,"log")

def main():
    paths = glob.glob(os.path.join(ROOT,"**","*.txt"), recursive=True)
    print(paths)
    for path in paths:
        # syslogファイルを読み込み
        with open(path, 'r') as infile, open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            for line in infile: # syslogの各行を解析して、必要なフィールドを抽出
                parts = line.split('|')
                writer.writerow(parsed_line)
                timestamp = parts[0] + ' ' + parts[1] + ' ' + parts[2] hostname = parts[3] process = parts[4].rstrip(':') message = ' '.join(parts[5:]) # 抽出したフィールドを辞書形式で保存 csv_data.append({ 'timestamp': timestamp, 'hostname': hostname, 'process': process, 'message': message })

    print("this ptyhon file path  ",ROOT)
    print("this ptyhon file path  ",SUBDIR)

if __name__ == "__main__":
    main()