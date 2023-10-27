import os

def main():
  print("Hola desde github actions!!!")
  token = os.environ.get("TOKEN_SECRETO")
  if not token:
    raise RuntimeError("TOKEN_SECRETO env var no esta puesto!!")
  print("Todo guay! encontramos nuestra env var")

if __name__ == '__main__':
        main()
