require 'optparse'

require 'capybara'
require 'nokogiri'

opts = ARGV.getopts 'o'
raise 'invalid args' if ARGV.parse!.size != 1
url = /^\d+/.match?(ARGV[0]) ? 'https://togetter.com/li/' + ARGV[0] : ARGV[0]

begin
    require 'selenium-webdriver'
    Capybara.register_driver :selenium do |app|
        options = Selenium::WebDriver::Chrome::Options.new
        options.add_argument('headless')
        options.add_argument('--log-level=2')
        Capybara::Selenium::Driver.new(app, browser: :chrome, options: options)
    end
    sess = Capybara::Session.new :selenium
    sess.visit url
rescue
    require 'capybara/poltergeist'
    Capybara.register_driver :poltergeist do |app|
        Capybara::Poltergeist::Driver.new(app, js_errors: false)
    end
    sess = Capybara::Session.new :poltergeist
    sess.visit url
end

loop do
    loop do
        sess.find('#more_tweet_btn').click rescue break
    end

    page = Nokogiri::HTML.parse(sess.html)
    page.css('.tweet_box .tweet').each do |e|
        puts e.text
        opts['o'] ? STDIN.gets : puts
    end

    sess.find('div.pagenation a[rel~=next]').click rescue break
end
