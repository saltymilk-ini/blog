import os
import sys

meta_info_marker = '---'
cnblog_link_marker = 'https://www.cnblogs.com/saltymilk/p/'


def create_directory(directory):
    try:
        return os.makedirs(directory, exist_ok=True)
    except Exception as e:
        print("error occurred when creating directory: {directory}:{e}")
        return False


def read_blog_source(blog_file_path):
    try:
        with open(blog_file_path, 'r', encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(
            f"error occurred when reading file: {blog_file_path}:{e}")


# extract meta info of an blog markdown file
def extract_meta_info(blog_text):
    meta_info = {}
    start = blog_text.find(meta_info_marker) + len(meta_info_marker)
    end = blog_text.find(meta_info_marker, start)

    meta_string = blog_text[start:end]
    for line in meta_string.splitlines():
        if ":" in line:
            tag, value = line.split(":", 1)
            stripped_tag = tag.strip()
            meta_info[stripped_tag] = value.strip()
            if (stripped_tag != 'Date'):
                continue
            
            # get month to create the archives
            date = value.strip()
            month = date[0, date.rfind('-')]
            meta_info['Archive'] = month

    return meta_info


# check if the meta info is valid
def check_meta_info(meta_info):
    required_keys = ['Author', 'Title', 'Category', 'Date', 'Summery']

    return all(key in meta_info for key in required_keys)


# redirect blog links to the deploy directory
def redirect_inner_linkage(blog_text, inner_directory):
    post = 0
    prev = 0
    redirected_text = ''

    while True:
        prev = blog_text.find(cnblog_link_marker, post)
        if prev == -1:
            break
        
        redirected_text += blog_text[post:prev]
        redirected_text += inner_directory

        post = prev+len(cnblog_link_marker)
        prev = blog_text.find('\"', post)
        # illegal text content
        if (prev == -1):
            return False
        
        target_file = blog_text[post:prev]
        if "#" not in target_file:
            target_file += '.html'
        else:
            # if the link contains an jump mark, insert suffix before the mark
            last_hash_pos = target_file.rfind('#')
            target_name = target_file[0 : last_hash_pos]
            target_file = target_name + '.html' + target_file[last_hash_pos:]
        
        redirected_text+=target_file
        post = prev

    if post !=-1:
        redirected_text += blog_text[post:]

    return True


# remove meta info and save the blog file as html file to target directory
def save_as_html(blog_text, dest_file_path):
    if not redirect_inner_linkage(blog_text,'./'):
        return False

    start = blog_text.find(meta_info_marker)
    end = blog_text.find(start+len(meta_info_marker))+len(meta_info_marker)
    html_text = blog_text[0:start]+blog_text[end:]

    try:
        with open(dest_file_path, "w", encoding="utf-8") as file:
            file.write(html_text)
        return True
    except Exception as e:
        print(f"error occurred when writing file: {dest_file_path}:{e}")
        return False

#create the main page html file
def create_main_page(meta_infos):
    #the fixed header
    html_text ={'<!DOCTYPE html>'
    '<html>'
    '<head>'
    '<meta charset="utf-8">'
    '<title>My Personal Blog</title>'
    '<link rel=\"stylesheet\" href=\"./css/style.css\">'
    '</head>'
    '<body>'
    '<h1>Welcome to visit my personal blog</h1>'
    '<h2></h2>'
    '<div class=\"container\">'
        '<main class=\"main_area\">'
            '<div class=\"blog-preview-area\">'}
    
    #add blog list to the main area
    for info in meta_infos:
        html_text+='<h2 class=\"blog-preview-title\">'
        html_text+=info["Title"]

#create the archive html files
def create_archive_pages(meta_infos):
    return

#create the category html files
def create_category_pages(meta_infos):
    return


def deploy(blog_source_path, deploy_path):
    deploy_sub_directories = [
        deploy_path+'/archives',
        deploy_path+'/blog_pages',
        deploy_path+'/categories']

    for directory in deploy_sub_directories:
        if not create_directory(directory):
            print("can not create necessary directories for deploying")
            return

    blog_meta_infos = []
    for root, _, files in os.walk(blog_source_path):
        for file in files:
            if not file.endswith('.md'):
                continue
            
            file_path = os.path.join(root, file)
            blog_text = read_blog_source(file_path)
            meta_info = extract_meta_info(blog_text)

            if not check_meta_info(meta_info):
                continue
            
            if not save_as_html(blog_text, deploy_sub_directories[1]):
                continue
            
            #this name is used to identify the blog source file
            file_name, _ = os.path.splitext(file)
            meta_info["Name"] = file_name

            blog_meta_infos.append(meta_info)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        deploy(sys.argv[0], sys.argv[1])
