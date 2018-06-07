# Backend Documentation

## Usage
### Requirements:
- python3
- filelock
- flask
- sqlite3

### Execution:
- tmux, create two windows
- python3 main.py
- python3 Kill_user.py

## API
- **Get** /lineup/:uid
    - return: success
        ```
        {
            'result': success,
            'room':roomcode

        }
        ```
    - return: fail
        ```
        {
            'result': fail
        }
        ```

- **Post** /record/:uid
    - content
    ```
    {
        'record': game_record(string)

    }
    ```
    - return
    ```
    {
        'result': success:fail

    }
        ```

## File structure

### backend
- config.py
    - config of flask backend
- db.lock
    - filelock for database
- user_gamedata.db3
    - Structure:
        - lineupPool (Unpaired users)
            - uid / timestamp(tick)
        - gameData (Postgame data)
            - id(AI) / uid / record
        - uid2room (Paired users)
            - uid / roomcode
- Kill_user.py
    - kill timeout users in a regular basis
    - timeout threshold: 15s
- main.py
    - main app for accepting requests
- Pairing.py
    - forked by main.py, pair up the Unpaired users
    - insert the paired user into uid2room
    - Pairup algorithm: FIFO
        - wait for +u to implement ML model
