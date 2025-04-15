FROM ruby:3.4.2

WORKDIR /home

COPY Gemfile ./


RUN gem install jekyll bundler && \
    bundle add logger &&\
    bundler install

 EXPOSE 4000

CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]

    # gem install dnsruby csv logger faraday faraday-retry && \
