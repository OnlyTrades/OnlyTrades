import csv

def split_csv_by_stock(input_file):
    # 打开输入 CSV 文件
    with open(input_file, 'r', newline='', encoding='utf-8') as fin:
        reader = csv.DictReader(fin)
        
        # 建立一个字典，用于存储不同 stock 对应的输出文件句柄和写入器
        stock_symbols = ['A', 'B', 'C', 'D', 'E']
        file_handles = {}
        csv_writers = {}
        
        try:
            # 初始化输出文件（A_stock.csv, B_stock.csv, ...），并写入表头
            for symbol in stock_symbols:
                output_file_name = f"{symbol}_stock.csv"
                fout = open(output_file_name, 'w', newline='', encoding='utf-8')
                writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
                
                # 写入 CSV 表头
                writer.writeheader()
                
                # 存储
                file_handles[symbol] = fout
                csv_writers[symbol] = writer
            
            # 逐行读取数据，并按照 stock 分类写入
            for row in reader:
                stock_symbol = row.get('stock', '')
                if stock_symbol in csv_writers:
                    csv_writers[stock_symbol].writerow(row)
        finally:
            # 确保脚本结束后关闭所有打开的输出文件
            for fout in file_handles.values():
                fout.close()

if __name__ == "__main__":
    # 替换成你的实际 CSV 文件名
    input_filename = 'featured_test_data.csv'
    split_csv_by_stock(input_filename)
