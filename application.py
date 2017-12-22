import os
from rrapp import app

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))    # pylint: disable=invalid-name
    app.run(host='0.0.0.0', port=port, threaded=True)
