import glob
import re

posts = glob.glob("/Users/hugosoares/blog_hsn_labs/docs/post/*.md")

count = 0
for p in posts:
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    
    parts = content.split("---")
    if len(parts) >= 3:
        frontmatter = parts[1]
        body = "---".join(parts[2:]).strip()
        
        # Remove first H1 if present
        body_lines = body.split("\n")
        new_body_lines = []
        removed_h1 = False
        for line in body_lines:
            if not removed_h1 and line.startswith("# "):
                removed_h1 = True
                continue
            new_body_lines.append(line)
            
        new_body = "\n".join(new_body_lines).strip()
        new_content = f"---\n{frontmatter.strip()}\n---\n\n{new_body}\n"
        with open(p, "w", encoding="utf-8") as f:
            f.write(new_content)
        count += 1

print(f"H1 duplicado removido de {count} posts.")
