from modules.interface import create_interface

if __name__ == "__main__":
    app = create_interface()
    app.launch(server_name="localhost", server_port=5000, share=False)
    