from src.shopify import shopify_streamingdata_functin
from src.weather import weather_streaming


def main():
    try:
        weather_streaming()
    except Exception as error:
        print(error)

    try:
        shopify_streamingdata_functin()
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()