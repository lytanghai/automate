FROM openjdk:17-jdk-alpine

# Set working directory inside the container
WORKDIR /app

# ARG allows us to pass the JAR name during build time if needed
ARG JAR_FILE=target/my-spring-boot-app.jar

# Copy the Spring Boot JAR file into the container as app.jar
COPY ${JAR_FILE} app.jar

# Expose the port your application runs on
EXPOSE 8080

# Define the command to run your application
ENTRYPOINT ["java", "-jar", "app.jar"]
