FROM httpd:2.4

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy configuration files
COPY httpd.conf /usr/local/apache2/conf/httpd.conf
COPY vhost.conf /usr/local/apache2/conf/extra/vhost.conf

# Create static directory
RUN mkdir -p /var/www/html/static

# Set permissions
RUN chown -R www-data:www-data /var/www/html

# Expose port
EXPOSE 80

# Start Apache
CMD ["httpd-foreground"] 