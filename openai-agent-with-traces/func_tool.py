from agents import Agent, Runner, trace, function_tool
import rich
from connection.myagent import config
import requests
import asyncio
from dotenv import load_dotenv
from typing import Union


# load_dotenv()

@function_tool
def add_func(num1 : int , num2 : int ):
    """ Add the two numbers and return the result
        Args : get num1 and num 2 from the prompt
    """

    return f'The sum of {num1} + {num2} is equal to {num1+num2}'

@function_tool
def multiply_func(num1 : int , num2 : int ):
    """ Multiply two numbers and return the result
        Args : get num1 and num 2 from the prompt
    """

    return f'The product of {num1} and {num2} is equal to {num1*num2}'

@function_tool
def get_weather(city: str):
    """Give dwtail weather on the city
    Args : get city name from the prompt
    """
    # Create the URL for the public weather service
    url = f"https://wttr.in/{city}?format=j1"

    # Send an HTTP GET request to wttr.in
    response = requests.get(url)
    data = response.json()  # Parse JSON response

    # Get current weather information
    current = data["current_condition"][0]

    # Return weather details as JSON
    return {
        "city": city,
        "temperature_C": current["temp_C"],
        "weather": current["weatherDesc"][0]["value"],
        "humidity": current["humidity"],
        "wind_speed_kmph": current["windspeedKmph"]
    }

@function_tool
def shopping_agent(
    product_name: str = None,
    price: Union[float, str, None] = None,
    price_above: Union[float, str, None] = None,
    price_below: Union[float, str, None] = None,
):
    """
    Flexible product search:
    - No parameters → return all products
    - Name only → filter by name
    - Price only → filter by exact price
    - Price range → filter by range
    - Name + Price filters → combine them
    """

    # Helper to safely convert input to float
    def to_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    # Convert parameters if needed
    price = to_float(price)
    price_above = to_float(price_above)
    price_below = to_float(price_below)

    url = "https://next-ecommerce-template-4.vercel.app/api/product"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        products = response.json().get("products", [])
    except requests.RequestException as e:
        return {"error": f"Error fetching products: {e}"}

    matching_products = []

    for p in products:
        product_price = float(p.get("price", 0))
        name_match = True
        price_match = True

        # Name filter
        if product_name:
            name_match = product_name.lower() in p.get("name", "").lower()

        # Price filters
        if price is not None:
            price_match = product_price == price
        else:
            if price_above is not None and product_price <= price_above:
                price_match = False
            if price_below is not None and product_price >= price_below:
                price_match = False

        if name_match and price_match:
            matching_products.append({
                "id": p.get("id"),
                "name": p.get("name"),
                "imagePath": p.get("imagePath"),
                "price": product_price,
                "description": p.get("description"),
                "discountPercentage": p.get("discountPercentage"),
                "isFeaturedProduct": p.get("isFeaturedProduct"),
                "stockLevel": p.get("stockLevel"),
                "category": p.get("category"),
            })

    count = len(matching_products)
    return {
        "count": count,
        "message": f"{count} product{'s' if count != 1 else ''} found.",
        "products": matching_products
    }

triage_agent = Agent(
    name = 'triage_agent',
    instructions =  
        """ You are a helpful assistant.use the appropriate tool.
            Otherwise, answer directly without using any tools.
        """,
    tools=[add_func,multiply_func,get_weather,shopping_agent],
    )

async def main():
    with trace('function_tool'):
        try:
            result = await Runner.run(
                            triage_agent, 
                            # 'Who is the founder of google',
                            # 'Who is the founder of facebook and sum of 2 and 8 and 3 multiply by 3',
                            # 'sum of 2 and 8 and 3 multiply by 3',
                            # 'multiply 4 by 4',
                            # "weather in karachi",
                            # "find Tribù Elio Chair",
                            # "find all chair",
                            # "find product price 850",
                            "find all chair below price 700",
                            # 'find products between 100 and 300 price',
                            # 'find chair of price 1200',
                            run_config=config,
                        )
        except Exception as e:
            print("Error" , e)
        else:
            rich.print("[RESULT]: ", result.final_output)

            # # If the tool returns a dictionary
            # if isinstance(result.final_output, dict) and "count" in result.final_output:
            #     print(f"✅ Total products found: {result.final_output['count']}")

            print("Last Agent ==> ", result.last_agent.name)

        finally:
                print("Execution Completed!")

if __name__ == "__main__":
    asyncio.run(main())



