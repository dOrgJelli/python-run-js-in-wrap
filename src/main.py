import sys
from polywrap import (
    Uri,
    PolywrapClient,
    PolywrapClientConfigBuilder,
    sys_bundle,
    web3_bundle
)

def main():

    # Create client to run wraps within
    config = (
        PolywrapClientConfigBuilder()
        .add_bundle(sys_bundle)
        .add_bundle(web3_bundle)
        .build()
    )

    client = PolywrapClient(config)

    # JS-Engine Wrap:
    # https://github.com/polywrap/js-engine-wrap/blob/main/wrap
    uri = Uri.from_str("ipfs/QmbDjF1Bw1UC1hToVxMMYsGeTYQCsmBqnW1xnTyHKkYLyr")
    method = "evalWithGlobals"

    # JS source
    source = """
    function fibonacci(n) {
        if (n <= 1) return n;

        let a = 0, b = 1;
        for (let i = 2; i <= n; i++) {
            const temp = a + b;
            a = b;
            b = temp;
        }
        return b;
    }

    fibonacci(num)
    """

    globals = [
        {
            "name": "num",
            "value": "8"
        }
    ]

    # Run the JS source within the JS-Engine wrap
    response = client.invoke(
        uri,
        method,
        args={
            "src": source,
            "globals": globals
        }
    )

    print(f"RESPONSE: {response}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(1)
    else:
        sys.exit(0)

