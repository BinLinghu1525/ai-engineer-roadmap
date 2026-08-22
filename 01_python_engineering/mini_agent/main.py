from agent import LearningSession


def main():
    session = LearningSession()
    message = session.complete_topic("  PYTHON agent  ")
    print(message)
    print(f"Completed topics: {session.completed_topics}")


if __name__ == "__main__":
    main()
