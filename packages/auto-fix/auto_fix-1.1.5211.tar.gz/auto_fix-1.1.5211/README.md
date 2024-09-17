使用方法 :
   from auto_fix import es
   
   
@es
def main():
    # 您的代码逻辑
    print("开始执行主程序")
    # 故意引入一个错误
    x = 1 / 0
    print("程序执行完毕")

if __name__ == '__main__':
    main()
	
但是运行之前 请务必设置 :
export OPENAI_API_KEY='your_openai_api_key'
export DEEPSEEK_API_KEY='your_deepseek_api_key'

Deepseek ai 他们的ai 个人认为非常好.所以就使用了他们的 如果您不喜欢可以设置none
另外一个就是openai 的api 