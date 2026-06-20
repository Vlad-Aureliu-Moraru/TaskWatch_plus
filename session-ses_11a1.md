# New session - 2026-06-20T16:33:46.373Z

**Session ID:** ses_11a1e6c7bffePuE3qItvixv7nj
**Created:** 6/20/2026, 7:33:46 PM
**Updated:** 6/20/2026, 7:37:21 PM

---

## User

hey so if i want to create an app similar to TaskWatch(https://github.com/Vlad-Aureliu-Moraru/TaskWatch) but to integrate better with my system , meaning i would want the timer to appear in my waybar and possibly have an ai agent to do some tasks from the app

---

## Assistant (Plan · DeepSeek V4 Flash Free · 5.4s)

_Thinking:_

The user wants to create an app similar to TaskWatch (a terminal task timer) but with:
1. Better system integration - timer appearing in Waybar (a status bar for Wayland compositors)
2. Possibly an AI agent to do tasks from the app

I'm in Plan Mode - I should only research and plan, not execute. Let me first explore what TaskWatch is, understand its architecture, and then think about how to design this.

Let me start by fetching the TaskWatch GitHub repo to understand its architecture, and also understand the Waybar integration possibilities.

**Tool: webfetch**

**Input:**
```json
{
  "url": "https://github.com/Vlad-Aureliu-Moraru/TaskWatch",
  "format": "markdown"
}
```

**Output:**
```
                       GitHub - Vlad-Aureliu-Moraru/TaskWatch: A modern to-do app with reminders and an adaptive Pomodoro timer, built with vanilla Java Swing. · GitHub                                             

[Skip to content](#start-of-content)   

## Navigation Menu

Toggle navigation

[](/)

[Sign in](/login?return_to=https%3A%2F%2Fgithub.com%2FVlad-Aureliu-Moraru%2FTaskWatch)

Appearance settings

  

-   Platform
    
    -   AI CODE CREATION
        
        -   [
            
            GitHub CopilotWrite better code with AI
            
            ](https://github.com/features/copilot)
        -   [
            
            GitHub Copilot appDirect agents from issue to merge
            
            ](https://github.com/features/ai/github-app)
        -   [
            
            MCP RegistryNewIntegrate external tools
            
            ](https://github.com/mcp)
        
    -   DEVELOPER WORKFLOWS
        
        -   [
            
            ActionsAutomate any workflow
            
            ](https://github.com/features/actions)
        -   [
            
            CodespacesInstant dev environments
            
            ](https://github.com/features/codespaces)
        -   [
            
            IssuesPlan and track work
            
            ](https://github.com/features/issues)
        -   [
            
            Code ReviewManage code changes
            
            ](https://github.com/features/code-review)
        
    -   APPLICATION SECURITY
        
        -   [
            
            GitHub Advanced SecurityFind and fix vulnerabilities
            
            ](https://github.com/security/advanced-security)
        -   [
            
            Code securitySecure your code as you build
            
            ](https://github.com/security/advanced-security/code-security)
        -   [
            
            Secret protectionStop leaks before they start
            
            ](https://github.com/security/advanced-security/secret-protection)
        
    -   EXPLORE
        
        -   [Why GitHub](https://github.com/why-github)
        -   [Documentation](https://docs.github.com)
        -   [Blog](https://github.blog)
        -   [Changelog](https://github.blog/changelog)
        -   [Marketplace](https://github.com/marketplace)
        
    
    [View all features](https://github.com/features)
    
-   Solutions
    
    -   BY COMPANY SIZE
        
        -   [Enterprises](https://github.com/enterprise)
        -   [Small and medium teams](https://github.com/team)
        -   [Startups](https://github.com/enterprise/startups)
        -   [Nonprofits](https://github.com/solutions/industry/nonprofits)
        
    -   BY USE CASE
        
        -   [App Modernization](https://github.com/solutions/use-case/app-modernization)
        -   [DevSecOps](https://github.com/solutions/use-case/devsecops)
        -   [DevOps](https://github.com/solutions/use-case/devops)
        -   [CI/CD](https://github.com/solutions/use-case/ci-cd)
        -   [View all use cases](https://github.com/solutions/use-case)
        
    -   BY INDUSTRY
        
        -   [Healthcare](https://github.com/solutions/industry/healthcare)
        -   [Financial services](https://github.com/solutions/industry/financial-services)
        -   [Manufacturing](https://github.com/solutions/industry/manufacturing)
        -   [Government](https://github.com/solutions/industry/government)
        -   [View all industries](https://github.com/solutions/industry)
        
    
    [View all solutions](https://github.com/solutions)
    
-   Resources
    
    -   EXPLORE BY TOPIC
        
        -   [AI](https://github.com/resources/articles?topic=ai)
        -   [Software Development](https://github.com/resources/articles?topic=software-development)
        -   [DevOps](https://github.com/resources/articles?topic=devops)
        -   [Security](https://github.com/resources/articles?topic=security)
        -   [View all topics](https://github.com/resources/articles)
        
    -   EXPLORE BY TYPE
        
        -   [Customer stories](https://github.com/customer-stories)
        -   [Events & webinars](https://github.com/resources/events)
        -   [Ebooks & reports](https://github.com/resources/whitepapers)
        -   [Business insights](https://github.com/solutions/executive-insights)
        -   [GitHub Skills](https://skills.github.com)
        
    -   SUPPORT & SERVICES
        
        -   [Documentation](https://docs.github.com)
        -   [Customer support](https://support.github.com)
        -   [Community forum](https://github.com/orgs/community/discussions)
        -   [Trust center](https://github.com/trust-center)
        -   [Partners](https://github.com/partners)
        
    
    [View all resources](https://github.com/resources)
    
-   Open Source
    
    -   COMMUNITY
        
        -   [
            
            GitHub SponsorsFund open source developers
            
            ](https://github.com/sponsors)
        
    -   PROGRAMS
        
        -   [Security Lab](https://securitylab.github.com)
        -   [Maintainer Community](https://maintainers.github.com)
        -   [Accelerator](https://github.com/accelerator)
        -   [GitHub Stars](https://stars.github.com)
        -   [Archive Program](https://archiveprogram.github.com)
        
    -   REPOSITORIES
        
        -   [Topics](https://github.com/topics)
        -   [Trending](https://github.com/trending)
        -   [Collections](https://github.com/collections)
        
    
-   Enterprise
    
    -   ENTERPRISE SOLUTIONS
        
        -   [
            
            Enterprise platformAI-powered developer platform
            
            ](https://github.com/enterprise)
        
    -   AVAILABLE ADD-ONS
        
        -   [
            
            GitHub Advanced SecurityEnterprise-grade security features
            
            ](https://github.com/security/advanced-security)
        -   [
            
            Copilot for BusinessEnterprise-grade AI features
            
            ](https://github.com/features/copilot/copilot-business)
        -   [
            
            Premium SupportEnterprise-grade 24/7 support
            
            ](https://github.com/premium-support)
        
    
-   [Pricing](https://github.com/pricing)

Search or jump to...

# Search code, repositories, users, issues, pull requests...

Search

Clear

[Search syntax tips](https://docs.github.com/search-github/github-code-search/understanding-github-code-search-syntax)

# Provide feedback

We read every piece of feedback, and take your input very seriously.

 Include my email address so I can be contacted

Cancel Submit feedback

# Saved searches

## Use saved searches to filter your results more quickly

Name  

Query 

To see all available qualifiers, see our [documentation](https://docs.github.com/search-github/github-code-search/understanding-github-code-search-syntax).

Cancel Create saved search

[Sign in](/login?return_to=https%3A%2F%2Fgithub.com%2FVlad-Aureliu-Moraru%2FTaskWatch)

[Sign up](/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F%3Cuser-name%3E%2F%3Crepo-name%3E&source=header-repo&source_repo=Vlad-Aureliu-Moraru%2FTaskWatch)

Appearance settings

Resetting focus

You signed in with another tab or window. Reload to refresh your session. You signed out in another tab or window. Reload to refresh your session. You switched accounts on another tab or window. Reload to refresh your session. Dismiss alert

[Vlad-Aureliu-Moraru](/Vlad-Aureliu-Moraru) / **[TaskWatch](/Vlad-Aureliu-Moraru/TaskWatch)** Public

-   [Notifications](/login?return_to=%2FVlad-Aureliu-Moraru%2FTaskWatch) You must be signed in to change notification settings
-   [Fork 0](/login?return_to=%2FVlad-Aureliu-Moraru%2FTaskWatch)
-   [Star 1](/login?return_to=%2FVlad-Aureliu-Moraru%2FTaskWatch)
    

-   [Code](/Vlad-Aureliu-Moraru/TaskWatch)
-   [Issues 0](/Vlad-Aureliu-Moraru/TaskWatch/issues)
-   [Pull requests 0](/Vlad-Aureliu-Moraru/TaskWatch/pulls)
-   [Actions](/Vlad-Aureliu-Moraru/TaskWatch/actions)
-   [Projects](/Vlad-Aureliu-Moraru/TaskWatch/projects)
-   [Security and quality 0](/Vlad-Aureliu-Moraru/TaskWatch/security)
-   [Insights](/Vlad-Aureliu-Moraru/TaskWatch/pulse)

Additional navigation options

-   [Code](/Vlad-Aureliu-Moraru/TaskWatch)
-   [Issues](/Vlad-Aureliu-Moraru/TaskWatch/issues)
-   [Pull requests](/Vlad-Aureliu-Moraru/TaskWatch/pulls)
-   [Actions](/Vlad-Aureliu-Moraru/TaskWatch/actions)
-   [Projects](/Vlad-Aureliu-Moraru/TaskWatch/projects)
-   [Security and quality](/Vlad-Aureliu-Moraru/TaskWatch/security)
-   [Insights](/Vlad-Aureliu-Moraru/TaskWatch/pulse)

 [](/Vlad-Aureliu-Moraru/TaskWatch)

# Vlad-Aureliu-Moraru/TaskWatch

 master

[Branches](/Vlad-Aureliu-Moraru/TaskWatch/branches)[Tags](/Vlad-Aureliu-Moraru/TaskWatch/tags)

[](/Vlad-Aureliu-Moraru/TaskWatch/branches)[](/Vlad-Aureliu-Moraru/TaskWatch/tags)

Go to file

Code

Open more actions menu

## Folders and files

Name

Name

Last commit message

Last commit date

## Latest commit

## History

[89 Commits](/Vlad-Aureliu-Moraru/TaskWatch/commits/master/)

[](/Vlad-Aureliu-Moraru/TaskWatch/commits/master/)89 Commits

[.github/workflows](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/.github/workflows "This path skips through empty directories")

[.github/workflows](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/.github/workflows "This path skips through empty directories")

[installer](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/installer "installer")

[installer](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/installer "installer")

[resources](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/resources "resources")

[resources](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/resources "resources")

[src](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src "src")

[src](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src "src")

[.gitignore](/Vlad-Aureliu-Moraru/TaskWatch/blob/master/.gitignore ".gitignore")

[.gitignore](/Vlad-Aureliu-Moraru/TaskWatch/blob/master/.gitignore ".gitignore")

[LICENSE](/Vlad-Aureliu-Moraru/TaskWatch/blob/master/LICENSE "LICENSE")

[LICENSE](/Vlad-Aureliu-Moraru/TaskWatch/blob/master/LICENSE "LICENSE")

[README.md](/Vlad-Aureliu-Moraru/TaskWatch/blob/master/README.md "README.md")

[README.md](/Vlad-Aureliu-Moraru/TaskWatch/blob/master/README.md "README.md")

[TaskWatch.ico](/Vlad-Aureliu-Moraru/TaskWatch/blob/master/TaskWatch.ico "TaskWatch.ico")

[TaskWatch.ico](/Vlad-Aureliu-Moraru/TaskWatch/blob/master/TaskWatch.ico "TaskWatch.ico")

[TaskWatch.jpg](/Vlad-Aureliu-Moraru/TaskWatch/blob/master/TaskWatch.jpg "TaskWatch.jpg")

[TaskWatch.jpg](/Vlad-Aureliu-Moraru/TaskWatch/blob/master/TaskWatch.jpg "TaskWatch.jpg")

[TaskWatch.png](/Vlad-Aureliu-Moraru/TaskWatch/blob/master/TaskWatch.png "TaskWatch.png")

[TaskWatch.png](/Vlad-Aureliu-Moraru/TaskWatch/blob/master/TaskWatch.png "TaskWatch.png")

View all files

## Repository files navigation

-   [README](#)
-   [GPL-3.0 license](#)

# TaskWatch

[](#taskwatch)

## Features

[](#features)

-   **Task Management** – create, edit, and organize your tasks in customizable lists
-   **Reminders** – get notified for important deadlines
-   **Adaptive Timer** – the time adapts based on the urgency and difficulty of the task
-   **Themes & Fonts** – clean UI with custom fonts and theme support
-   **Cross-Platform** – works on **Linux** and **Windows**

---

## Usage

[](#usage)

-   `:h` → opens the **help menu**
-   `` ` `` → goes **back in the menu**

### File Structure

[](#file-structure)

-   Create **📁 Folders** in the main menu with `:a`
-   Each **📁 Folder** contains its own **📓 Tasks**
-   Each **📓 Task** can have its own **🗒️ Notes**

---

## Installation

[](#installation)

### Linux

[](#linux)

1.  Download the latest **Linux tarball** from [Releases](https://github.com/Vlad-Aureliu-Moraru/TaskWatch/releases).
2.  Extract it:
    
    tar -xvzf TaskWatch-<version\>\-Linux.tar.gz
    cd TaskWatch
    ./install-scripts/install.sh/
    

### Windows

[](#windows)

1.  Download the latest **Exe** from [Releases](https://github.com/Vlad-Aureliu-Moraru/TaskWatch/releases).

## About

A modern to-do app with reminders and an adaptive Pomodoro timer, built with vanilla Java Swing.

### Resources

[Readme](#readme-ov-file)

### License

[GPL-3.0 license](#GPL-3.0-1-ov-file)

### Uh oh!

There was an error while loading. Please reload this page.

[Activity](/Vlad-Aureliu-Moraru/TaskWatch/activity)

### Stars

[**1** star](/Vlad-Aureliu-Moraru/TaskWatch/stargazers)

### Watchers

[**0** watching](/Vlad-Aureliu-Moraru/TaskWatch/watchers)

### Forks

[**0** forks](/Vlad-Aureliu-Moraru/TaskWatch/forks)

[Report repository](/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2FVlad-Aureliu-Moraru%2FTaskWatch&report=Vlad-Aureliu-Moraru+%28user%29)

## [Releases 33](/Vlad-Aureliu-Moraru/TaskWatch/releases)

[

TaskWatch v1.4.0 Latest

Dec 18, 2025



](/Vlad-Aureliu-Moraru/TaskWatch/releases/tag/1.4.0)

[\+ 32 releases](/Vlad-Aureliu-Moraru/TaskWatch/releases)

## [Packages 0](/users/Vlad-Aureliu-Moraru/packages?repo_name=TaskWatch)

### Uh oh!

There was an error while loading. Please reload this page.

## [Contributors](/Vlad-Aureliu-Moraru/TaskWatch/graphs/contributors)

### Uh oh!

There was an error while loading. Please reload this page.

## Languages

-   [Java 97.2%](/Vlad-Aureliu-Moraru/TaskWatch/search?l=java)
-   [Shell 2.8%](/Vlad-Aureliu-Moraru/TaskWatch/search?l=shell)

## Footer

[](https://github.com)© 2026 GitHub, Inc.

### Footer navigation

-   [Terms](https://docs.github.com/site-policy/github-terms/github-terms-of-service)
-   [Privacy](https://docs.github.com/site-policy/privacy-policies/github-privacy-statement)
-   [Security](https://github.com/security)
-   [Status](https://www.githubstatus.com/)
-   [Community](https://github.community/)
-   [Docs](https://docs.github.com/)
-   [Contact](https://support.github.com?tags=dotcom-footer)
-   Manage cookies
-   Do not share my personal information

You can’t perform that action at this time.
```

**Tool: webfetch**

**Input:**
```json
{
  "url": "https://github.com/Vlad-Aureliu-Moraru/TaskWatch/blob/main/README.md",
  "format": "markdown"
}
```

**Error:**
```
StatusCode: non 2xx status code (404 GET https://github.com/Vlad-Aureliu-Moraru/TaskWatch/blob/main/README.md)
```

---

## Assistant (Plan · DeepSeek V4 Flash Free · 4.2s)

_Thinking:_

Let me look at the source code of TaskWatch to understand its architecture better, and also research Waybar custom integrations and how AI agents can be integrated.

**Tool: webfetch**

**Input:**
```json
{
  "format": "markdown",
  "url": "https://github.com/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src"
}
```

**Output:**
```
                       TaskWatch/src at master · Vlad-Aureliu-Moraru/TaskWatch · GitHub                                             

[Skip to content](#start-of-content)   

## Navigation Menu

Toggle navigation

[](/)

[Sign in](/login?return_to=https%3A%2F%2Fgithub.com%2FVlad-Aureliu-Moraru%2FTaskWatch%2Ftree%2Fmaster%2Fsrc)

Appearance settings

  

-   Platform
    
    -   AI CODE CREATION
        
        -   [
            
            GitHub CopilotWrite better code with AI
            
            ](https://github.com/features/copilot)
        -   [
            
            GitHub Copilot appDirect agents from issue to merge
            
            ](https://github.com/features/ai/github-app)
        -   [
            
            MCP RegistryNewIntegrate external tools
            
            ](https://github.com/mcp)
        
    -   DEVELOPER WORKFLOWS
        
        -   [
            
            ActionsAutomate any workflow
            
            ](https://github.com/features/actions)
        -   [
            
            CodespacesInstant dev environments
            
            ](https://github.com/features/codespaces)
        -   [
            
            IssuesPlan and track work
            
            ](https://github.com/features/issues)
        -   [
            
            Code ReviewManage code changes
            
            ](https://github.com/features/code-review)
        
    -   APPLICATION SECURITY
        
        -   [
            
            GitHub Advanced SecurityFind and fix vulnerabilities
            
            ](https://github.com/security/advanced-security)
        -   [
            
            Code securitySecure your code as you build
            
            ](https://github.com/security/advanced-security/code-security)
        -   [
            
            Secret protectionStop leaks before they start
            
            ](https://github.com/security/advanced-security/secret-protection)
        
    -   EXPLORE
        
        -   [Why GitHub](https://github.com/why-github)
        -   [Documentation](https://docs.github.com)
        -   [Blog](https://github.blog)
        -   [Changelog](https://github.blog/changelog)
        -   [Marketplace](https://github.com/marketplace)
        
    
    [View all features](https://github.com/features)
    
-   Solutions
    
    -   BY COMPANY SIZE
        
        -   [Enterprises](https://github.com/enterprise)
        -   [Small and medium teams](https://github.com/team)
        -   [Startups](https://github.com/enterprise/startups)
        -   [Nonprofits](https://github.com/solutions/industry/nonprofits)
        
    -   BY USE CASE
        
        -   [App Modernization](https://github.com/solutions/use-case/app-modernization)
        -   [DevSecOps](https://github.com/solutions/use-case/devsecops)
        -   [DevOps](https://github.com/solutions/use-case/devops)
        -   [CI/CD](https://github.com/solutions/use-case/ci-cd)
        -   [View all use cases](https://github.com/solutions/use-case)
        
    -   BY INDUSTRY
        
        -   [Healthcare](https://github.com/solutions/industry/healthcare)
        -   [Financial services](https://github.com/solutions/industry/financial-services)
        -   [Manufacturing](https://github.com/solutions/industry/manufacturing)
        -   [Government](https://github.com/solutions/industry/government)
        -   [View all industries](https://github.com/solutions/industry)
        
    
    [View all solutions](https://github.com/solutions)
    
-   Resources
    
    -   EXPLORE BY TOPIC
        
        -   [AI](https://github.com/resources/articles?topic=ai)
        -   [Software Development](https://github.com/resources/articles?topic=software-development)
        -   [DevOps](https://github.com/resources/articles?topic=devops)
        -   [Security](https://github.com/resources/articles?topic=security)
        -   [View all topics](https://github.com/resources/articles)
        
    -   EXPLORE BY TYPE
        
        -   [Customer stories](https://github.com/customer-stories)
        -   [Events & webinars](https://github.com/resources/events)
        -   [Ebooks & reports](https://github.com/resources/whitepapers)
        -   [Business insights](https://github.com/solutions/executive-insights)
        -   [GitHub Skills](https://skills.github.com)
        
    -   SUPPORT & SERVICES
        
        -   [Documentation](https://docs.github.com)
        -   [Customer support](https://support.github.com)
        -   [Community forum](https://github.com/orgs/community/discussions)
        -   [Trust center](https://github.com/trust-center)
        -   [Partners](https://github.com/partners)
        
    
    [View all resources](https://github.com/resources)
    
-   Open Source
    
    -   COMMUNITY
        
        -   [
            
            GitHub SponsorsFund open source developers
            
            ](https://github.com/sponsors)
        
    -   PROGRAMS
        
        -   [Security Lab](https://securitylab.github.com)
        -   [Maintainer Community](https://maintainers.github.com)
        -   [Accelerator](https://github.com/accelerator)
        -   [GitHub Stars](https://stars.github.com)
        -   [Archive Program](https://archiveprogram.github.com)
        
    -   REPOSITORIES
        
        -   [Topics](https://github.com/topics)
        -   [Trending](https://github.com/trending)
        -   [Collections](https://github.com/collections)
        
    
-   Enterprise
    
    -   ENTERPRISE SOLUTIONS
        
        -   [
            
            Enterprise platformAI-powered developer platform
            
            ](https://github.com/enterprise)
        
    -   AVAILABLE ADD-ONS
        
        -   [
            
            GitHub Advanced SecurityEnterprise-grade security features
            
            ](https://github.com/security/advanced-security)
        -   [
            
            Copilot for BusinessEnterprise-grade AI features
            
            ](https://github.com/features/copilot/copilot-business)
        -   [
            
            Premium SupportEnterprise-grade 24/7 support
            
            ](https://github.com/premium-support)
        
    
-   [Pricing](https://github.com/pricing)

Search or jump to...

# Search code, repositories, users, issues, pull requests...

Search

Clear

[Search syntax tips](https://docs.github.com/search-github/github-code-search/understanding-github-code-search-syntax)

# Provide feedback

We read every piece of feedback, and take your input very seriously.

 Include my email address so I can be contacted

Cancel Submit feedback

# Saved searches

## Use saved searches to filter your results more quickly

Name  

Query 

To see all available qualifiers, see our [documentation](https://docs.github.com/search-github/github-code-search/understanding-github-code-search-syntax).

Cancel Create saved search

[Sign in](/login?return_to=https%3A%2F%2Fgithub.com%2FVlad-Aureliu-Moraru%2FTaskWatch%2Ftree%2Fmaster%2Fsrc)

[Sign up](/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F%3Cuser-name%3E%2F%3Crepo-name%3E%2Ffiles%2Fdisambiguate&source=header-repo&source_repo=Vlad-Aureliu-Moraru%2FTaskWatch)

Appearance settings

Resetting focus

You signed in with another tab or window. Reload to refresh your session. You signed out in another tab or window. Reload to refresh your session. You switched accounts on another tab or window. Reload to refresh your session. Dismiss alert

[Vlad-Aureliu-Moraru](/Vlad-Aureliu-Moraru) / **[TaskWatch](/Vlad-Aureliu-Moraru/TaskWatch)** Public

-   [Notifications](/login?return_to=%2FVlad-Aureliu-Moraru%2FTaskWatch) You must be signed in to change notification settings
-   [Fork 0](/login?return_to=%2FVlad-Aureliu-Moraru%2FTaskWatch)
-   [Star 1](/login?return_to=%2FVlad-Aureliu-Moraru%2FTaskWatch)
    

-   [Code](/Vlad-Aureliu-Moraru/TaskWatch)
-   [Issues 0](/Vlad-Aureliu-Moraru/TaskWatch/issues)
-   [Pull requests 0](/Vlad-Aureliu-Moraru/TaskWatch/pulls)
-   [Actions](/Vlad-Aureliu-Moraru/TaskWatch/actions)
-   [Projects](/Vlad-Aureliu-Moraru/TaskWatch/projects)
-   [Security and quality 0](/Vlad-Aureliu-Moraru/TaskWatch/security)
-   [Insights](/Vlad-Aureliu-Moraru/TaskWatch/pulse)

Additional navigation options

-   [Code](/Vlad-Aureliu-Moraru/TaskWatch)
-   [Issues](/Vlad-Aureliu-Moraru/TaskWatch/issues)
-   [Pull requests](/Vlad-Aureliu-Moraru/TaskWatch/pulls)
-   [Actions](/Vlad-Aureliu-Moraru/TaskWatch/actions)
-   [Projects](/Vlad-Aureliu-Moraru/TaskWatch/projects)
-   [Security and quality](/Vlad-Aureliu-Moraru/TaskWatch/security)
-   [Insights](/Vlad-Aureliu-Moraru/TaskWatch/pulse)

 [](/Vlad-Aureliu-Moraru/TaskWatch)

## FilesExpand file tree

 master

## Breadcrumbs

1.  [TaskWatch](/Vlad-Aureliu-Moraru/TaskWatch/tree/master)

/

# src

/

Copy path

## Directory actions

## More options

More options

## Directory actions

## More options

More options

## Latest commit

## History

[History](/Vlad-Aureliu-Moraru/TaskWatch/commits/master/src)

[](/Vlad-Aureliu-Moraru/TaskWatch/commits/master/src)History

 master

## Breadcrumbs

1.  [TaskWatch](/Vlad-Aureliu-Moraru/TaskWatch/tree/master)

/

# src

/

Copy path

Top

## Folders and files

Name

Name

Last commit message

Last commit date

### parent directory

[

..

](/Vlad-Aureliu-Moraru/TaskWatch/tree/master)

[Archive](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/Archive "Archive")

[Archive](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/Archive "Archive")

[Directory](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/Directory "Directory")

[Directory](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/Directory "Directory")

[Logic](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/Logic "Logic")

[Logic](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/Logic "Logic")

[Note](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/Note "Note")

[Note](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/Note "Note")

[Task](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/Task "Task")

[Task](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/Task "Task")

[UserInterface](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/UserInterface "UserInterface")

[UserInterface](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/UserInterface "UserInterface")

[app](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/app "app")

[app](/Vlad-Aureliu-Moraru/TaskWatch/tree/master/src/app "app")

View all files

## Footer

[](https://github.com)© 2026 GitHub, Inc.

### Footer navigation

-   [Terms](https://docs.github.com/site-policy/github-terms/github-terms-of-service)
-   [Privacy](https://docs.github.com/site-policy/privacy-policies/github-privacy-statement)
-   [Security](https://github.com/security)
-   [Status](https://www.githubstatus.com/)
-   [Community](https://github.community/)
-   [Docs](https://docs.github.com/)
-   [Contact](https://support.github.com?tags=dotcom-footer)
-   Manage cookies
-   Do not share my personal information

You can’t perform that action at this time.
```

**Tool: websearch**

**Input:**
```json
{
  "query": "TaskWatch pomodoro timer Java architecture"
}
```

**Output:**
```
Title: abadongutierrez/pomodoro-timer
URL: https://github.com/abadongutierrez/pomodoro-timer
Published: 2025-11-04T01:02:18.000Z
Author: N/A
Highlights:
# Repository: abadongutierrez/pomodoro-timer

Small Pomodoro Timer implementing Hexagonal Architecture

- Stars: 4
- Forks: 0
- Watchers: 4
- Open issues: 1
- Primary language: Java
- Languages: Java (98.9%), Shell (0.6%), Batchfile (0.5%)
- Default branch: main
- Created: 2025-11-04T01:02:18Z
- Last push: 2025-11-04T22:49:41Z
- Contributors: 1 (top: abadongutierrez)

---

# 🍅 Pomodoro Timer

A Pomodoro Timer built with JavaFX and Spring Shell using **Hexagonal Architecture**.

That means, Core is encapsulated and exposed only using Ports implemented by Adapters.

## ✨ Features

### 🎯 Core Functionality

- **Pomodoro Technique** - 25-minute work sessions with 5-minute breaks
- **Long Breaks** - 15-minute break after 4 completed Pomodoros
- **Daily Statistics** - Tracks completed Pomodoros per day
- **Persistent Stats** - Saves your progress to disk

## 🏗️ Architecture

This project uses **Hexagonal Architecture** (Ports & Adapters) for:

- ✅ Clean separation of concerns
- ✅ Framework independence (domain layer has no JavaFX)
- ✅ Easy testing (mockable ports)
- ✅ Flexibility (swap implementations easily)

### Layer Structure

```
📦 pomodoro-timer 
├── 🟢 domain/                  # Pure business logic
├── 🔵 application/             # Use cases & ports
│   ├── port/in/                # Driving ports
│   ├── port/out/               # Driven ports
│   ├── dto/                    # Dtos
│   └── service/                # Port In Implementation
│
├── 🟡 adapters/                 # Framework integration
└── config/
```

---

## 🚀 Getting Started

### Prerequisites

- Java 21+
- Maven 3.6+

### Build & Run

```bash
# Compile and install
mvn clean install
cd app-bootstrap

# Run using JavaFX
./run-javafx.sh

# or

# Run using spring shell
./run-shell.sh
```

---

## 🎮 Usage

### JavaFX

1. Launch the app
2. Click **Start** to begin a 25-minute Pomodoro
3. Or adjust the minute spinner for custom duration

#### Controls

- **Start/Resume** - Begin or continue timer
- **Pause** - Pause the countdown
- **Reset** - Stop and reset to initial time

### Shell

1. Launch the app
2. type `timer start` or `timer start ` to start a custom pomodoro
3. type `timer status` to see the current timer status or `timer watch` to "watch" the pomodoro timer

type `help` to see other commands

---

## 📂 Data Storage

- History is saved in `~/.pomodoro-timer/timer-history.json`
- Create the directory if it doesn't exist

---

---

## 🔧 Configuration

WIP

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🚧 Future Enhancements

- [ ] Add AI
- [ ] Add Blockchain
- [ ] Add Bluetooth

j/k WIP

---

---

Title: 2b33rs/pomowatch
URL: https://github.com/2b33rs/pomowatch
Published: 2023-01-28T16:03:14.000Z
Author: N/A
Highlights:
# Repository: 2b33rs/pomowatch

- Stars: 1
- Forks: 0
- Watchers: 1
- Open issues: 0
- Primary language: Java
- Languages: Java
- Default branch: master
- Created: 2023-01-28T16:03:14Z
- Last push: 2023-03-21T18:24:55Z
- Contributors: 1 (top: 2b33rs)

---

# Pomodoro Timer

![](https://freesvg.org/storage/img/thumb/lmproulx-Timer-Minuterie.png)

This project is a simple Pomodoro Timer application built using Java with JavaFX. The main purpose of the application is to provide a local solution for managing time while studying, cooking, or performing any activity that requires focused work.

## How to use

The application is easy to use. Simply launch the executable file, and you will be presented with a window containing a timer. The default timer is set to 25 minutes, which is the recommended duration for a Pomodoro session. You can adjust the timer duration to suit your needs by clicking on the "Settings" button.

Once you have set the timer duration, you can start the timer by clicking on the "Start" button. The timer will count down the time and will display a notification when the time is up. You can pause or stop the timer at any time by clicking on the corresponding buttons.
Features

The application provides the following features:

- Customizable timer duration
 - Start, pause, and stop buttons
 - Notification when the timer completes
 - User-friendly interface built using JavaFX

## How to run

To run the application, you need to have Java installed on your machine. You can download Java from the official website: https://www.java.com/en/download/

Once you have Java installed, you can download the executable JAR file from the repository. To run the JAR file, open the terminal, navigate to the directory containing the JAR file, and run the following command:

```
java -jar pomodoro-timer.jar
```

## Contributing

This project is open source, and contributions are welcome. If you find any bugs or have any feature requests, please create an issue on the repository's issue tracker.

## License

This project is licensed under the MIT License. You can read the license file for more information.

---

Title: danishmohammed/focusApp
URL: https://github.com/danishmohammed/focusApp
Published: 2022-01-23T19:35:57.000Z
Author: N/A
Highlights:
# Repository: danishmohammed/focusApp

- Stars: 0
- Forks: 0
- Watchers: 1
- Open issues: 0
- Primary language: Java
- Languages: Java
- Default branch: main
- Homepage: https://medium.com/@danishmohammed57/i-made-a-focus-productivity-app-b49195430417
- Created: 2022-01-23T19:35:57Z
- Last push: 2024-07-21T19:43:03Z
- Contributors: 1 (top: danishmohammed)

---

# Focus App

The Focus App is a Java-based productivity tool designed to help users manage tasks and improve focus through effective time management techniques. The main functionalities of the app include task management and the Pomodoro timer. I wrote an article about it [here](https://danishmohammed57.medium.com/i-made-a-focus-productivity-app-b49195430417)

 
 
 
 

## Features

- **Task Management**: Add, edit, and delete tasks with ease.
- **Pomodoro Timer**: Use the Pomodoro technique to improve focus and productivity.

## Technologies Used

- **Java**
- **Java Swing**: For the graphical user interface (GUI).

## Download the App

To use the Focus App:

1. **Download the JAR file**: Ensure you have JDK installed.
2. **Run the JAR file**: Double-click the downloaded JAR file to start the application. NOTE: If you are on Mac, make sure the jar file is saved to the parent dir of Downloads (its usually your name, e.g. danishmohammed) otherwise the storage mechanism will not work properly.

If you want to see and modify the code, download the ZIP file from the repository.

For more information on using the app, refer to this [link](https://drive.google.com/file/d/1O9jzvfanLfHIUHbX0XoR1Bnyoxo4wmyu/view)

## Contact

For any questions or feedback, please contact me through my website: [danishmohammed.ca](https://danishmohammed.ca)

---

Title: tientrinh21/Tomadoro
URL: https://github.com/tientrinh21/Tomadoro
Published: 2022-06-28T17:01:21.000Z
Author: N/A
Highlights:
# Repository: tientrinh21/Tomadoro

Pomodoro-based task management app

- Stars: 1
- Forks: 0
- Watchers: 1
- Open issues: 0
- Primary language: Java
- Languages: Java
- Default branch: master
- Created: 2022-06-28T17:01:21Z
- Last push: 2023-12-27T04:36:54Z
- Contributors: 1 (top: tientrinh21)

---

# 🍅 Tomadoro - Pomodoro-based task management app

Tomadoro is an app help students keep track of todo tasks and let them focus on studying with Pomodoro method.

## Table of contents

- [Screenshots](#screenshots)
- [Built with](#built-with)
- [Demo](#demo)
- [Author](#author)

## Screenshots

![Screenshot 1](./screenshots/screenshot_1.png)
![Screenshot 2](./screenshots/screenshot_2.png)
![Screenshot 4](./screenshots/screenshot_4.png)
![Screenshot 3](./screenshots/screenshot_3.png)

## Built with

- Java (Netbeans GUI Builder)
- [FlatLaf - Flat Look and Feel](https://www.formdev.com/flatlaf/)

## Demo

You can try the apps by downloading the repo and run this code (Java need to be installed).

```
javac -classpath ".:Tomadoro.jar:target/dependency/*"  . Achievement.java Main.java Music.java Pomodoro.java
java -classpath ".:Final.jar:target/dependency/*" Main
```

## Author

- Website - [Tien Trinh](https://tientrinh.netlify.app/)

---

Title: Search code, repositories, users, issues, pull requests...
URL: https://github.com/mousaabougrich/simple-task.pomdoro-app-backend
Published: 2024-08-02T15:25:31.000Z
Author: mousaabougrich
Highlights:
Task Management Application with Pomodoro Timer
...
This is a Spring Boot-based application designed to help users manage tasks and time using a Pomodoro timer. The application allows users to create, update, delete, and view tasks, as well as manage user roles and authentication using JWT (JSON Web Token).
Note: I'm still learning Spring Boot, Java, and web development in general, so this project is a work in progress. I'm happy if anyone wants to upgrade the app, contribute a frontend, or provide tips to help me learn more!
Features
...
Tasks by Status:
...
their status (e.g., TODO, IN\_PROGRESS, DONE).
2. Pomodoro Timer
...
Start Pomodoro Session: A user can start a Pomodoro session which will run for a specified duration (typically 25 minutes).
Break Sessions: After completing a Pomodoro session, users can take short or long breaks depending on the number of Pomodoro sessions completed.
3. User Management
...
Prerequisites
Java 17 or later
Maven
...
MySQL or any other relational database
...
Add Task: POST /api/tasks
Update Task: PUT /api/tasks/{id}
Delete Task: DELETE /api/tasks/{id}
View Tasks by Person: GET /api/tasks/person/{personId}
View Tasks by Status: GET /api/tasks/status/{status}
3. Pomodoro Timer
...
Start Pomodoro: POST /api/pomodoro/start
Check Status: GET /api/pomodoro/status
Running Tests

---

Title: aditya-7562/PomodoroTimer
URL: https://github.com/aditya-7562/PomodoroTimer
Published: 2025-07-10T08:40:38.000Z
Author: N/A
Highlights:
A Pomodoro-style productivity timer built with a robust backend using Spring Boot and Java, and a responsive, user-friendly frontend developed using HTML, CSS, and JavaScript. This tool helps users stay focused by alternating between work sessions and short breaks, following the Pomodoro Technique.
...
Pomodoro Timer is a web-based productivity application that implements the Pomodoro Technique. This time management method uses a timer to break work into intervals, traditionally 25 minutes in length, separated by short breaks. This application helps users manage their work sessions, track productivity, and maintain focus.
...
- **Customizable Timer**: Focus sessions (25 minutes) and break sessions
- **Task Management**: Add descriptions to your Pomodoro sessions
- **Session Tracking**: Record completed sessions and view productivity statistics
- **User Authentication**: Secure login and registration system
- **User Profiles**: Personalized dashboard and settings
- **Responsive Design**: Works on desktop and mobile devices
- **Audio Notifications**: Sound alerts when sessions end
...
- **Java 21**: Core programming language
- **Spring Boot 3.2.3**: Application framework
- **Spring Security**: Authentication and authorization
- **Spring Data JPA**: Database access and ORM
- **Hibernate**: Object-relational mapping
- **SQLite**: Development database
- **PostgreSQL**: Production database option
- **Lombok**: Reduces boilerplate code
- **Maven**: Dependency management and build tool
...
- **Thymeleaf**: Server-side Java template engine
- **Tailwind CSS**: Utility-first CSS framework
- **JavaScript**: Client-side functionality
- **Tone.js**: Audio feedback library
...
## Project Structure
...
```
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/pomodoro/app/
│   │   │       ├── config/        # Application configuration
│   │   │       ├── controller/    # MVC controllers
│   │   │       ├── dto/           # Data transfer objects
│   │   │       ├── model/         # Entity models
│   │   │       ├── repository/    # Data access layer
│   │   │       └── service/       # Business logic
│   │   └── resources/
│   │       ├── static/            # CSS, JavaScript
│   │       ├── templates/         # Thymeleaf templates
│   │       └── application.properties # App configuration
└── pom.xml                        # Maven dependencies
```
...
- Java Development Kit (JDK) 2
...
The application uses SQLite for development by default. The database file will be created automatically in the project root directory.

---

Title: codemnky/pomtask
URL: https://github.com/codemnky/pomtask
Published: 2011-12-25T04:00:20.000Z
Author: N/A
Highlights:
# Repository: codemnky/pomtask

Pomodoro task management application

- Stars: 4
- Forks: 0
- Watchers: 2
- Open issues: 0
- Primary language: Java
- Languages: Java (96.4%), Groovy (3.6%)
- Default branch: master
- Created: 2011-12-25T04:00:20Z
- Last push: 2012-01-23T23:37:19Z
- Contributors: 1 (top: codemnky)

---

# Pomtask

Pomtask is a task tool built around the [Pomodoro Technique](http://www.pomodorotechnique.com/).

## Building

Build the application:

```
gradle build
```

To run the rest web services:

```
cd web-rest
gradle cargoRunLocal
```

Go to: http://localhost:9090/test

---

Title: VidhyaVarshanyJS/DailyTaskScheduler
URL: https://github.com/VidhyaVarshanyJS/DailyTaskScheduler
Published: N/A
Author: VidhyaVarshanyJS
Highlights:
# VidhyaVarshanyJS/DailyTaskScheduler

A Simple Java task management system to schedule tasks weekly along with a pomodoro timer 

- Stars: 1
- Forks: 2
- Watchers: 1
- Open issues: 0
- License: MIT License
- Default branch: master
- Created: 2022-11-02T11:19:13Z

## Languages

- Java

## Top Contributors

- VidhyaVarshanyJS (25 contributions)

---

## README

# Daily Task Scheduler

## About

A Simple Java task management system to schedule tasks weekly along with a pomodoro timer that effectively manages daily keeps work track on time. It is built with Java Swings for UI and entire code is written in Java.This Application is basically a GUI version of [TODLIST](https://github.com/VidhyaVarshanyJS/TODOLIST-CONSOLE) with some additional features.It has CRUD operations which are done using SQL database .A Pomodoro timer also included in this application to enhance the productivity to track the time on a specific task by the user.This Task Scheduler schedules the task according to the the week days in accordance with the system date and time . 

**Keywords:** java , java-swing , MySQL

## Table of contents

> * [About](#about--synopsis)
> * [Table of contents](#table-of-contents)
> * [Dependency](#dependency)
> * [Installation](#installation)
> * [Working](#working)
> * [More Reference](#more-reference)
> * [License](#license)

### Dependency

- Windows(above 7/8/10/11) x64bit
- Apache NetBeans 12.0
- Xampp Web-Server
- mysql-connector library 8.0.27 jsr file
- Java JDK Version 14

## Installation

- Create database of name `test_days_database` in MyPhPAdmin after starting the Apache and the MySql from Xampp Server 
- Give the correct username and password inside the `Prerequisite.java` file .Database Tables will be created automatically
 
 

 

 
 Fig.1 - Username , password ,Database name 

### Working

https://user-images.githubusercontent.com/76642252/199493172-3af8c69b-bdb5-43be-97ac-21f1b163c85e.mp4

### More Reference

[Daily Task Scheduler.pdf](https://github.com/VidhyaVarshanyJS/DailyTaskScheduler/blob/1a3c85cf9180288d2f78b16ad44c3ed7ecf0358f/Daily%20Task%20Scheduler.pdf)

## License

Licensed at [MIT](https://choosealicense.com/licenses/mit/)
```

**Tool: websearch**

**Input:**
```json
{
  "query": "waybar custom timer integration custom module scripting 2025 2026"
}
```

**Output:**
```
Title: Module: Custom · Alexays/Waybar Wiki · GitHub
URL: https://github.com/alexays/waybar/wiki/Module:-Custom
Published: N/A
Author: Alexays
Highlights:
The`custom` module displays either the output of a script or static text. To display static text, specify only the`format` field.
...
| option | typeof | default | description |
| --- | --- | --- | --- |
| `exec` | string |
| `exec-if` | string | The path to a script, which determines if the script in`exec` should be executed.`exec` will be executed if the exit code of`exec-if` equals 0. |
...
| `exec-on-event` | bool | `true` | If an event command is set (e.g.`on-click` or`on-scroll-up`) then re-execute the script. There are no guarantees that`exec` is executed after the`on-*` event commands finished. See https://github.com/Alexays/Waybar/pull/1784 for a possible patch. |
...
| `interval` | integer | The interval (in seconds) in which the information gets polled.Use`once` if you want to execute the module only on startup. You can update it manually with a signal. If no`interval` is defined, it is assumed that the out script loops it self. |
...
| `restart-interval` | integer | The restart interval (in seconds).Can't be used with the interval option, so only with continuous scripts.Once the script exit, it'll be re-executed after the restart-interval. |
...
| `signal` | integer | The signal number used to update the module. The number is valid between 1 and N, where`SIGRTMIN+N`=`SIGRTMAX`. |
...
| `format` | string | `{}` | The format, how information should be displayed. On`{}` data gets inserted. |
...
| `on-click` | string | Command to execute when clicked on the module. |
...
| `on-click-middle` | string | Command to execute when you middle clicked on the module using mousewheel. |
| `on-click-right` | string | Command to execute when you right clicked on the module. |
...
| `on-scroll-up` | string | Command to execute when scrolling up on the module. |
| `on-scroll-down` | string | Command to execute when scrolling down on the module. |
...
| `smooth-scrolling-threshold` | double | Threshold to be used when scrolling. |
...
| `tooltip` | bool | `true` | Option to enable
...
| `tooltip-format` | string
...
escape` | bool | `false` |
...
The`exec` script may be continuous (i.e. contain some kind of infinite loop). The display will be updated for each new line of data on stdout (following the chosen`return-type`).
...
The`interval` option does not work with continuous script (no need to call it several times… as it will continuously run). However you might want to set the`restart-interval` to start again the script if it stops after some time.
...
The`{}` placeholder is special: it automatically displays the text output from your script. However,`{}` cannot be combined with other placeholders like`{icon}` in the format string — using both together will not work as expected.
...
interval` parameter

---

Title: jbirnick/waybar-timer
URL: https://github.com/jbirnick/waybar-timer
Published: N/A
Author: N/A
Highlights:
> [!NOTE] 
> This used to be a shell script. Now it is a binary.
> The CLI arguments have changed only slightly but the underlying architecture is completely different.
> Therefore, if you switch from the shell script version to the binary, please make sure to **fully adapt the new default config**.
...
> In particular, you need to add `hook` for `exec`, remove `interval`, set `exec-on-event` to false, and change `increase -60` to `decrease 60`.
...
> You also need to start a waybar-timer server _before_ you start waybar.
...
You can **customize behaviour and appearance in a simple way**.
...
1. Download the binary from the [releases](https://github.com/jbirnick/waybar-timer/releases) (or build it yourself with cargo) and put it in a directory of your choice (e.g. `~/.scripts/`).
2. In the startup script of your compositor, run `/path/to/waybar_timer serve` and make sure it starts **before waybar starts**.
3. Copy-paste the [example configuration](#example-configuration) from below into your waybar config and style it.
4. Customize. (see [Customization section](#customization))
...
```json
"custom/timer": {
    "exec": "/path/to/waybar_timer hook",
    "exec-on-event": false,
    "return-type": "json",
    "format": "{icon} {0}",
    "format-icons": {
        "standby": "STANDBY",
        "running": "RUNNING",
        "paused": "PAUSE"
    },
    "on-click": "/path/to/waybar_timer new 25 'notify-send \"Session finished\"'",
    "on-click-middle": "/path/to/waybar_timer cancel",
    "on-click-right": "/path/to/waybar_timer togglepause",
    "on-scroll-up": "/path/to/waybar_timer increase 60 || /path/to/waybar_timer new 1 'notify-send -u critical \"Timer expired\"'",
    "on-scroll-down": "/path/to/waybar_timer decrease 60"
}
...
Furthermore you can style the module using the `timer` class, for example:
...
## Customization
...
The example configuration implements a 25min "pomodoro session" timer with left click, pausing with right click, canceling with middle click, and an unnamed timer by just scrolling up from the standby mode.
...
You can customize the different numbers and names to your own flavor and needs. To understand what the commands do and to implement some different behaviour see the [documentation](#documentation).
...
_before_ you start waybar
...
- #### `hook`
 This is the command which you want to put in your waybar `exec` field.
 It subscribes to the server to get all the updates of the timer.
 Updates are delivered as JSON which is readable by waybar.
...
there is no timer active
...
change the state
...
_start a new timer_.
...
> You can implement this because
...
increase` will exit with code 1
...
there is no current timer, so you can do:
...
pkill` to send signals to

---

Title: niraletter/waybar-timer
URL: https://github.com/nirabyte/waybar-timer
Published: 2026-01-12T18:09:17.000Z
Author: N/A
Highlights:
A highly efficient, timer and pomodoro module for Waybar with mouse controls and CLI commands.
...
- **Dual Mode: Standard Timer and Pomodoro** with customizable work/break cycles
- Mouse and CLI controls (toggle, pause, resume, reset, skip)
- Desktop notifications and sound effects
- Dynamic visual feedback with state-specific icons and colors
- Customizable presets and helpful tooltips
- Persistent state across Waybar restarts, syncs across multiple waybar instances
- minimal system resource footprint
...
Add or update to waybar config (~/.config/waybar/config.jsonc)**
...
```jsonc
   // place the module
   "modules-left": [
        "custom/timer"
    ],
...
// define the module
   "custom/timer": {
       "exec": "~/.config/waybar/scripts/timer.sh",
       "return-type": "json",
       "format": "{}",
       "on-click": "~/.config/waybar/scripts/timer.sh click",
       "on-click-right": "~/.config/waybar/scripts/timer.sh right",
       "on-click-middle": "~/.config/waybar/scripts/timer.sh middle",
       "on-scroll-up": "~/.config/waybar/scripts/timer.sh down",
       "on-scroll-down": "~/.config/waybar/scripts/timer.sh up",
       "tooltip": true,
       "escape": true
   }
   ```
...
You can customize the script to use different sounds for different events by editing the sound variables in `timer.sh`:
...
```bash
    SOUND_TIMER_DONE="${HOME}/.config/waybar/sounds/timer.mp3"
    SOUND_WORK_START="${HOME}/.config/waybar/sounds/timer.mp3"
    SOUND_BREAK_START="${HOME}/.config/waybar/sounds/timer.mp3"
    SOUND_BREAK_END="${HOME}/.config/waybar/sounds/timer.mp3"
    SOUND_COMPLETE="${HOME}/.config/waybar/sounds/timer.mp3"
   ```
...
The script uses `paplay` (compatible with both PulseAudio and PipeWire) to play sounds.
...
### CLI commands
...
**Pomodoro:**
...
Edit the top of `timer.sh` to customize timer presets, scroll seconds, auto break/work, inactivity time, and sound effects:
...
# Pomodoro Settings
POMO_ENABLED=true
POMO_AUTO_BREAK=true
POMO_AUTO_WORK=true
...
# --- SOUND EFFECTS ---
SOUND_TIMER_DONE="${HOME}/.config/waybar/sounds/timer.mp3"
...
SOUND_WORK_START="${HOME}/.config/waybar/
...
/timer.mp3"
...
_BREAK_START="${HOME}/.config/waybar/
...
/timer.mp3"
...
_BREAK_END="${HOME}/.config/waybar/
...
/timer.mp3"
...
_COMPLETE="${HOME}/.config/waybar/
...
/timer.mp3"
...
## Notifications & Sounds
...
When a timer or pomodoro session completes, the script sends a notification via `notify-send` and plays a sound effect via `paplay`.
...
**Advanced customization (multiple sound files):**
...
Edit the sound variables in `timer.sh` to use different sounds for different events:
...
- **Work session
...
:** `break_start.
...
- **Break
...
, back to work:** `work_start.
...
- **All sessions complete:**

---

Title: Module: Custom: Examples · Alexays/Waybar Wiki · GitHub
URL: https://github.com/Alexays/Waybar/wiki/Module:-Custom:-Examples
Published: N/A
Author: Alexays
Highlights:
# Module: Custom: Examples
...
astrysm edited this page Feb 25, 2026 · 3 revisions
...
This page contains brief examples, with code provided here directly, of custom modules:
...
```
"custom/cpuhistory": {
  "exec": "~/.config/waybar/scripts/cpu_history.py -d 60",
  "format": "<span color='#FFA500'>  </span>{}",
  "interval": 1,
  "return-type": "json",
  "on-click": "~/.config/waybar/scripts/cpu_history.py toggle"
},
```
...
#### dunst:
...
```
"custom/dunst": {
    "exec": "~/.config/waybar/scripts/dunst.sh",
    "on-click": "dunstctl set-paused toggle",
    "restart-interval": 1,
}
...
#### NVIDIA GPU (with nvidia
...
": "nvidia
...
gpu=utilization
...
temperature.gpu
...
]\\+\\), \\([0
...
]\\+\\)/\\
...
🌡️\\
...
°C/g
...
```
"custom/media": {
    "format": "{icon} {}",
    "escape": true,
    "return-type": "json",
    "max-length": 40,
    "on-click": "playerctl play-pause",
    "on-click-right": "playerctl stop",
    "smooth-scrolling-threshold": 10, // This value was tested using a trackpad, it should be lowered if using a mouse.
    "on-scroll-up": "playerctl next",
    "on-scroll-down": "playerctl previous",
    "exec": "$HOME/.config/waybar/mediaplayer.py 2> /dev/null", // Script in resources/custom_modules folder
}
...
spotify": {
    "format": "{icon} {}",
    "escape": true,
    "return-type": "json",
    "max-length": 40,
    "interval": 30, // Remove this if your script is endless and write in loop
    "on-
...
": "player
...
p spotify play-pause",
    "on-click-right": "killall spotify",
    "smooth-scrolling-threshold": 10, // This value was tested using a trackpad, it should be lowered if using a mouse
...
"on-scroll-up" : "player
...
-p spotify next",
    "on-scroll-down" : "player
...
-p spotify previous",
    "exec": "$HOME/.config/waybar/mediaplayer.py 2> /dev/null", // Script in resources/custom_modules folder
    "exec-if":
...
spotify"
}
...
"$HOME/.
...
#### Pacman
...
```
"custom/pacman": {
    "format": "{}  ",
    "interval": "once",
    "exec": "pacman_packages",
    "on-
...
update-system",
    "signal
...
every hour
...
updates
...
RTMIN+
...
", // update
...
"
...
~/.config/
...
/config`
...
```
"custom/weather": {
    "exec": "${HOME}/.config/waybar/scripts/get_weather.sh Berlin+Germany",
    "return-type": "json",
    "format": "{}",
    "
...
": true,
    "
...
#### Sway Scratchpad Indicator:
...
scratchpad-indicator
...
interval": 3,
    "return-type": "json",
    "exec":
...
swaymsg
...
#### Sway output scaling toggle

---

Title: huzefa12/waybar-timer
URL: https://github.com/huzefa12/waybar-timer
Published: 2026-01-26T01:40:47.000Z
Author: N/A
Highlights:
⏲️ Enhance your productivity with Waybar Timer, an efficient Pomodoro timer featuring mouse controls and CLI commands for seamless task management.
...
- Stars: 1
- Forks: 0
- Watchers: 1
- Open issues: 0
- Primary language: Shell
- Languages: Shell
- License: MIT License (MIT)
- Topics: arch-wa, cli, hyde, hyprland, omarchy, omarchy-mac, omarchy-waybar, omarchytheme, pomodoro, quickshell, ricing, timer, waybar, waybar-config, waybar-minimal, waybar-module, waybar-omarchy, wayland
- Default branch: main
- Homepage: https://huzefa12.github.io
- Created: 2026-01-26T01:40:47Z
- Last push: 2026-04-05T18:03:45Z
- Contributors: 2 (top: niraletter, huzefa12)
...
# ⏳ waybar-timer - Flexible Timer for Your Workflow
...
Welcome to waybar-timer! This application provides a flexible timer and pomodoro module specifically designed for Waybar. With easy mouse controls and command-line interface (CLI) commands, you can manage your time effectively and boost your productivity.
...
- **Flexible Timer Options**: Customize your timers based on your needs.
- **Pomodoro Support**: Utilize the popular Pomodoro technique to enhance focus and efficiency.
- **Mouse Controls**: Easily start, stop, and reset timers using your mouse.
- **CLI Commands**: Use simple commands for advanced users who prefer the terminal.
...
- **Operating System**: Linux
- **Waybar**: Ensure that you have Waybar installed and properly configured.
- **Dependencies**: The application requires basic libraries available on most Linux distributions.
...
1. **Run the Application**: After installation, you can run waybar-timer through your application menu, or by typing `waybar-timer` in your terminal.
...
## 📖 Usage Instructions
...
1. Click on the waybar-timer icon on your Waybar.
2. Choose the duration you want the timer to run.
3. Press the "Start" button to begin.
...
### Using Pomodoro Technique
...
To set a Pomodoro timer:
...
1. Select the Pomodoro option from the menu.
2. The timer will automatically set to 25 minutes. You can change the duration if needed.
3. Start the timer and work on your task. After the time is up, you will receive a notification.
...
### Using CLI Commands
...
For advanced users, you can also control the timer using commands in the terminal. Here are some basic commands:
...
- **Start Timer**:
...
```bash
  waybar-timer start 25
  ```
...
- **Stop Timer**:
...
```bash
  waybar-timer stop
  ```
...
- **Reset Timer**:
...
```bash
  waybar-timer reset
  ```

---

Title: refactor(custom): move continuous exec onto GLib command stream  · Pull Request #4915 · Alexays/Waybar
URL: https://github.com/Alexays/Waybar/pull/4915
Published: 2026-03-09T04:04:18.000Z
Author: khaneliman
Highlights:
## refactor(custom): move continuous exec onto GLib command stream
...
`custom` used two different blocking paths that could stall module updates.

For continuous commands, the module read stdout with a blocking getline()
 loop. That worked for simple cases, but it kept long-running custom scripts
 tied to a worker thread that could sit indefinitely waiting for a newline or
 EOF.
...
For interval- and signal-driven custom modules, refreshes also synchronously
 waited on previously launched event children before running the next update.
 If an older on-click/on-scroll child was still alive, the next refresh could
 be delayed behind that wait.
...
This change addresses both cases:

- continuous custom commands now run through a GLib main-loop-backed command
 stream instead of a blocking FILE*/getline() loop
 - interval refreshes now reap old event children with waitpid(..., WNOHANG)
 instead of blocking on them
...
Tested with some simple custom modules:
...
```json
  "custom/test-github-reap": {
    "exec": "sh -c 'printf \"{\\\"text\\\":\\\"%s\\\"}\\n\" \"$(date +%T)\"'",
    "format": " (gh {text}) ",
    "interval": 5,
    "on-click": "sleep 20",
    "return-type": "json",
    "tooltip": false
  },
  "custom/test-hyprsunset-reap": {
    "exec": "sh -c 'printf \"{\\\"text\\\":\\\"%s\\\",\\\"alt\\\":\\\"%s\\\"}\\n\" \"$(date +%T)\" \"$(date +%S)\"'",
    "format": "( {text} )",
    "tooltip-format": "sec {alt}",
    "interval": 3600,
    "signal": 1,
    "on-click": "sleep 20",
    "on-scroll-up": "sleep 20",
    "return-type": "json"
  },
```
...
- test-github-reap
 Click it once.
 Keep watching for 20 seconds.
 On this branch: the timestamp keeps updating every 5 seconds while the
 sleep 20 child is still running.
 Current code, the module freezes until that child exits.

- test-hyprsunset-reap
 Click or scroll it once.
 Immediately run:

`pkill -RTMIN+1 waybar`

On this branch: it updates right away. Current code will not update as the signal-driven refresh waits behind the sleeping
 child.
...
**Austin Horstman** pushed commit `078efc8`: feat(util): add GLib command stream for nonblocking line reads; pushed commit `bfe333d`: test(util): cover command stream line delivery and EOF flushing · Mar 9, 2026 at 3:30am
...
**Austin Horstman** pushed commit `ec705f5`: refactor(custom): move continuous exec onto GLib command stream · Mar 9, 2026 at 3:32am
...
**Austin Horstman** pushed commit `f693a21`: fix(custom): avoid blocking child reaps in interval worker · Mar 9, 2026 at 3:33am
...
**Austin Horstman** pushed commit `504220c`: fix(util): keep GLib child setup fork-safe · Mar 9, 2026 at 1pm
...
> Sorry, keep meaning to come back to this to figure out the freebsd path error.

---

Title: Streaming JSON in `custom/*` modules no longer renders any text.
URL: https://github.com/Alexays/Waybar/issues/4522
Published: N/A
Author: N/A
Highlights:
# Streaming JSON in `custom/*` modules no longer renders any text.
...
Streaming **JSON** in `custom/*` modules no longer renders text. Plain-text streaming is unaffected.

Any `custom/*` that runs a long-lived command emitting continuous **JSON** frames to stdout (with `"return-type": "json"` and `"interval": 0`) appears as an **empty label** on the bar. Polling / one-shot commands still render.
...
This also breaks common patterns like `swaync-client -swb` (see: [SwayNotificationCenter Waybar example](https://github.com/ErikReider/SwayNotificationCenter?tab=readme-ov-file#waybar-example)).
...
- Built-in modules render normally.
- Non-streaming `custom/*` (exec returns once per interval) render normally.
- Affected examples in my setup:
 - `custom/cava` (audio visualizer stream)
 - `custom/notifications` (e.g., `swaync-client -swb`)
...
- GTK widget tree shows the module label nodes (e.g., `label#custom-cava.module`), but the visible text is blank.
- Waybar logs show **no JSON parse errors** when the JSON is valid, and no other runtime errors.
- Replacing the stream with a **polled one-shot** (e.g., piping to `head -n1` or adding a `--once` flag) restores visible output immediately.
- **Plain-text streaming works** (when `return-type` is omitted and raw text is formatted).
- **JSON streaming fails only** when `return-type: "json"` **and** `interval: 0` (long-lived process).
...
Last known good: source build from **late Sep 2025**. 
Broken after rebuilding from source on **Oct 1–2, 2025**.
...
2. Use this Waybar config (streaming, `interval: 0`):

   ```jsonc
   {
     "layer": "top",
     "position": "top",
     "modules-left": ["custom/cava"],
     "custom/cava": {
       "exec": "python3 -u ~/.config/waybar/scripts/fake_cava.py",
       "return-type": "json",
       "interval": 0,
       "restart-interval": 0,
       "format": "{text}",
       "escape": true,
       "tooltip": false
     }
   }
   ```

3. Launch Waybar and observe: the `custom/cava` label exists in the widget tree, but **no text is rendered**.
...
Streaming `custom/*` modules that continuously emit valid JSON frames should render their text, as in previous versions.
...
> Brilliant!
> 
> Thanks for the quick fix. I built your PR and verified it works and solves the issue 👍🏻 
> 
> It also **solves the recent performance hits with static `custom/*` modules as well** 🥇
> 
> ---
> 
> > [!NOTE]
> >
> > In my steps to reproduce config, I used `"interval": 0` for a continuous stream. 
> >
> > That config worked in previous Waybar versions, but with this change now you need to **omit** `interval` for continuous streaming ([per the documentation](https://github.com/Alexays/Waybar/wiki/Module:-Custom#continuous-script)).

---

Title: If signal is defined in a custom module for a self-updating command. the module never loads · Issue #3976 · Alexays/Waybar
URL: https://github.com/Alexays/Waybar/issues/3976
Published: 2025-03-08T18:52:57.000Z
Author: gsgleason
Highlights:
## If signal is defined in a custom module for a self-updating command. the module never loads
...
> This is what the manpage waybar-custom says for `signal`:
> "If no interval is defined then a signal will be the only way to update the module."
> 
> So the behaviour you're observing seems to be intended. Perhaps there could be a new feature that provides an option `force-exec-on-load` or something.
...
> The options are not mutually exclusive. But if you have
> 
> ```
> "custom/test": {
> "exec": "./date-test.sh",
> "signal": 1,
> }
> ```
> 
> custom module will use a waitingWorker, for
> 
> ```
> "custom/test": {
> "exec": "./date-test.sh",
> "signal": 1,
> "interval":"once"
> }
> ```
> 
> (or any other interval) it will use a delayWorker and for
> 
> ```
> "custom/test": {
> "exec": "./date-test.sh",
> "signal": 1,
> "restart-interval":5
> }
> ```
> 
> it will use a continuousWorker. I've tested this with some [trace output](https://github.com/RobertMueller2/Waybar/tree/custom-test) (could have used a debugger, but I like trace output). As far as I can tell, only the continuousWorker is really suited for continuous script output, the other two kinda expect that the script exits. The first and the second can be woken up by a signal. I don't think anything happens for the signal when using a continuousWorker.
...
interval, restart-interval
...
> 
> - use `"worker-type": "delay"` if you want to execute a script with a given interval. Supports signal, exec-if and exec-on-event.
> - use `"worker-type": "waiting"` if you want to execute a script initially and upon receiving a signal. Supports signal, exec-if and exec-on-event
...
> - use `"worker-type":"continuous"` if you want to listen for continuous script output.
...
> 
> and then throw errors for invalid combinations instead of inherently and intransparently choosing different worker types. But someone would have to change that and advocate the fact it would be a breaking change. ;) Perhaps in place of that the manpage could reflect sensible combinations or what triggers which worker/mode.
...
> 
> I think right now your options are:
> 
> - use the first example with a non-continuous script. As far as I've observed, it'll initially populate the module and it can then be updated by signal. The deciding portion is that the script exits. Kinda what you want to achieve?
> - use the second example with a non-continuous script and any interval (the workaround you already have)
...
> 
> p.S.: The separate implementation for signal without interval was added in #2517. I was wrong about the interpretation of the manpage as far as the initial execution if concerned, but the "only updated by signal" part seems to be intended beyond the initial execution.
```

---

## Assistant (Plan · DeepSeek V4 Flash Free · 166.8s)

_Thinking:_

Now I have a good understanding of the landscape. Let me analyze this further:

1. **TaskWatch** is a Java Swing desktop app with:
   - Task management (CRUD)
   - Reminders
   - Adaptive Pomodoro timer (adjusts based on urgency/difficulty)
   - Themes & fonts
   - Cross-platform (Linux/Windows)

2. **Waybar integration** - Waybar has a `custom` module that can execute scripts and display their output. There are existing waybar-timer projects (like jbirnick/waybar-timer, niraletter/waybar-timer) that show how to integrate a timer with Waybar.

3. **AI agent** - The user wants an AI agent that can perform tasks from the app.

Let me think about the architecture:

For a Linux-focused app that integrates with Waybar:
- The app needs a backend/service that runs persistently
- A CLI tool or IPC mechanism to communicate between Waybar and the app
- Waybar's custom module can run a script that reads from the app's state
- The AI agent could be integrated via local LLM (like Ollama) or API-based

Let me think about the best tech stack and architecture:

**Option 1: Python**
- Fast to develop
- Rich ecosystem for CLI, TUI, and web frameworks
- Libraries for desktop notifications (notify2, dbus)
- Easy IPC via sockets, DBus, or files
- AI integration via OpenAI API, Ollama, etc.

**Option 2: Rust**
- Performance and low resource usage
- Good for a system-level daemon
- Can be compiled to a single binary
- Growing ecosystem for TUI (ratatui) and CLI

**Option 3: Go**
- Easy cross-compilation
- Good concurrency model
- Single binary output
- Good for daemon/services

**Option 4: Keep Java but modernize**
- TaskWatch is Java Swing
- Could refactor to a client-server model
- But Java isn't great for lightweight system integration

I think the best approach would be:

**Recommended: Python or Rust**

Let me draft a comprehensive plan.

**Architecture:**

1. **Backend Daemon** - A persistent background service that manages:
   - Timer state (pomodoro sessions, breaks)
   - Task database
   - AI agent integration
   
2. **IPC Mechanism** - Unix socket or DBus for communication between components

3. **Waybar Integration** - A small script/binary that connects to the daemon and outputs JSON for Waybar

4. **CLI Client** - Command-line tool to control the daemon (start/pause/resume timer, add/list tasks)

5. **TUI/GUI** - Optional terminal UI or GUI for task management

6. **AI Agent** - Integration with Ollama (local) or OpenAI API for:
   - Task suggestions based on context
   - Automatic task breakdown
   - Smart reminders
   - Natural language task creation

Let me think about specifics:

**Waybar Integration Strategy:**
The daemon writes state to a file (e.g., `/tmp/taskwatch-state.json`) or provides it via a socket. Waybar's `custom` module runs a script that reads this state and outputs JSON like:
```json
{"text": "🍅 25:00", "alt": "focus", "tooltip": "Focus session\nTask: Write report", "class": "running"}
```

The Waybar module config would look like:
```json
"custom/taskwatch": {
    "exec": "taskwatch waybar",
    "exec-on-event": false,
    "return-type": "json",
    "format": "{icon} {}",
    "format-icons": {
        "standby": "⏸",
        "running": "▶",
        "paused": "⏸",
        "break": "☕"
    },
    "on-click": "taskwatch toggle",
    "on-click-right": "taskwatch new 25",
    "on-click-middle": "taskwatch cancel"
}
```

**AI Agent Integration:**
- Local model via Ollama (Llama 3, Mistral, etc.)
- Or OpenAI/Anthropic API
- Key capabilities:
  1. Natural language task creation: "Add task to review PR by tomorrow"
  2. Task prioritization suggestions
  3. Automatic Pomodoro duration suggestions based on task complexity
  4. Daily/weekly productivity summaries
  5. Context-aware break reminders

Let me formulate the plan properly.

Actually, let me ask the user some clarifying questions first to narrow down the approach before presenting a plan.

Great, I've researched TaskWatch, Waybar custom module integration, and existing waybar-timer projects. Let me ask a few questions to nail down the architecture before I present a plan.

**Tool: question**

**Input:**
```json
{
  "questions": [
    {
      "question": "What tech stack do you prefer for building this? TaskWatch uses Java Swing, but for Waybar integration something more lightweight makes sense.",
      "header": "Preferred tech stack",
      "options": [
        {
          "label": "Python",
          "description": "Fast to develop, great for CLI/daemon, easy AI integration via Ollama/OpenAI, good IPC libraries"
        },
        {
          "label": "Rust",
          "description": "Single binary, minimal resources, excellent for system daemons, growing TUI ecosystem"
        },
        {
          "label": "Go",
          "description": "Easy cross-compilation, good concurrency, single binary, solid CLI tooling"
        },
        {
          "label": "Keep Java (refactored)",
          "description": "Keep the Java core but add a lightweight IPC layer for Waybar integration"
        }
      ]
    },
    {
      "question": "For the AI agent, do you want it to run locally or use cloud APIs?",
      "header": "AI agent approach",
      "options": [
        {
          "label": "Local LLM (Ollama)",
          "description": "Run models like Llama 3, Mistral locally via Ollama — fully offline, no API costs"
        },
        {
          "label": "Cloud API (OpenAI/Anthropic)",
          "description": "Use GPT-4, Claude, etc. via API — more capable but requires internet and API key"
        },
        {
          "label": "Both (configurable)",
          "description": "Support both local and cloud backends, user picks at runtime"
        }
      ]
    },
    {
      "question": "What AI features are most important to you?",
      "header": "AI features",
      "multiple": true,
      "options": [
        {
          "label": "Natural language task creation",
          "description": "\"Add task to review PR by Friday\""
        },
        {
          "label": "Smart Pomodoro duration",
          "description": "AI suggests work/break lengths based on task complexity"
        },
        {
          "label": "Task suggestions/prioritization",
          "description": "AI suggests what to work on next based on deadlines and priorities"
        },
        {
          "label": "Productivity summaries",
          "description": "Daily/weekly reports on time spent and task completion"
        },
        {
          "label": "Autonomous task execution",
          "description": "AI agent can actually execute tasks (e.g., git operations, file edits)"
        }
      ]
    }
  ]
}
```

**Output:**
```
User has answered your questions: "What tech stack do you prefer for building this? TaskWatch uses Java Swing, but for Waybar integration something more lightweight makes sense."="Python", "For the AI agent, do you want it to run locally or use cloud APIs?"="i would want something like opencode", "What AI features are most important to you?"="Autonomous task execution, Task suggestions/prioritization". You can now continue with the user's answers in mind.
```

---

## Assistant (Plan · DeepSeek V4 Flash Free · 9.8s)

_Thinking:_

The user wants:
1. Python as the tech stack
2. AI agent like opencode - meaning they want an AI coding agent integrated with the task timer system. opencode is the CLI tool I'm running as. It's a tool for software engineering tasks. So the AI agent should be able to execute coding tasks autonomously, similar to opencode.
3. Autonomous task execution and task suggestions/prioritization as top AI features

So the vision is:
- A task timer/system that integrates with Waybar
- An AI agent (like opencode) that can autonomously execute coding tasks from the task list
- The AI agent can also suggest what tasks to work on and prioritize them

This is quite ambitious! Let me think about the architecture carefully.

The key insight is that the user wants something like opencode integrated into a TaskWatch-like app. So the AI agent would:
1. Read tasks from the task list
2. Execute appropriate actions (code edits, git operations, etc.)
3. Report back completion status
4. Get spawned from the task timer app context

Let me design the architecture:

**Project Structure:**
```
taskwatch/
├── taskwatch/              # Python package
│   ├── __init__.py
│   ├── __main__.py         # CLI entry point
│   ├── daemon.py           # Background daemon
│   ├── timer.py            # Pomodoro timer logic
│   ├── tasks.py            # Task management (CRUD, storage)
│   ├── waybar.py           # Waybar JSON output formatter
│   ├── ipc.py              # Unix socket IPC
│   ├── storage.py          # SQLite/JSON persistence
│   └── agent/
│       ├── __init__.py
│       ├── core.py         # Agent core (like opencode's agent)
│       ├── tools.py        # Tool definitions (file ops, git, etc.)
│       └── llm.py          # LLM integration (Ollama/OpenAI)
├── config/                 # Example configs
├── scripts/                # Helper scripts
├── pyproject.toml          # Package metadata
└── README.md
```

**Waybar Integration:**
- Daemon runs as a systemd user service
- Writes state to a Unix socket or a file
- Waybar custom module runs `taskwatch waybar` which reads state and outputs JSON
- CLI tool `taskwatch` controls everything

**AI Agent:**
- Similar to opencode's agent architecture
- Tools: read/write files, run commands, git operations, web search
- Uses Ollama or OpenAI API
- Can be triggered on tasks, or can proactively suggest tasks

Let me look more at what opencode does to understand the agent architecture better.

**Tool: webfetch**

**Input:**
```json
{
  "url": "https://opencode.ai",
  "format": "markdown"
}
```

**Output:**
```
OpenCode | The open source AI coding agent

[![OpenCode](data:image/svg+xml,%3csvg%20width='234'%20height='42'%20viewBox='0%200%20234%2042'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M18%2030H6V18H18V30Z'%20fill='%23CFCECD'/%3e%3cpath%20d='M18%2012H6V30H18V12ZM24%2036H0V6H24V36Z'%20fill='%23656363'/%3e%3cpath%20d='M48%2030H36V18H48V30Z'%20fill='%23CFCECD'/%3e%3cpath%20d='M36%2030H48V12H36V30ZM54%2036H36V42H30V6H54V36Z'%20fill='%23656363'/%3e%3cpath%20d='M84%2024V30H66V24H84Z'%20fill='%23CFCECD'/%3e%3cpath%20d='M84%2024H66V30H84V36H60V6H84V24ZM66%2018H78V12H66V18Z'%20fill='%23656363'/%3e%3cpath%20d='M108%2036H96V18H108V36Z'%20fill='%23CFCECD'/%3e%3cpath%20d='M108%2012H96V36H90V6H108V12ZM114%2036H108V12H114V36Z'%20fill='%23656363'/%3e%3cpath%20d='M144%2030H126V18H144V30Z'%20fill='%23CFCECD'/%3e%3cpath%20d='M144%2012H126V30H144V36H120V6H144V12Z'%20fill='%23211E1E'/%3e%3cpath%20d='M168%2030H156V18H168V30Z'%20fill='%23CFCECD'/%3e%3cpath%20d='M168%2012H156V30H168V12ZM174%2036H150V6H174V36Z'%20fill='%23211E1E'/%3e%3cpath%20d='M198%2030H186V18H198V30Z'%20fill='%23CFCECD'/%3e%3cpath%20d='M198%2012H186V30H198V12ZM204%2036H180V6H198V0H204V36Z'%20fill='%23211E1E'/%3e%3cpath%20d='M234%2024V30H216V24H234Z'%20fill='%23CFCECD'/%3e%3cpath%20d='M216%2012V18H228V12H216ZM234%2024H216V30H234V36H210V6H234V24Z'%20fill='%23211E1E'/%3e%3c/svg%3e)![OpenCode](data:image/svg+xml,%3csvg%20width='234'%20height='42'%20viewBox='0%200%20234%2042'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M18%2030H6V18H18V30Z'%20fill='%234B4646'/%3e%3cpath%20d='M18%2012H6V30H18V12ZM24%2036H0V6H24V36Z'%20fill='%23B7B1B1'/%3e%3cpath%20d='M48%2030H36V18H48V30Z'%20fill='%234B4646'/%3e%3cpath%20d='M36%2030H48V12H36V30ZM54%2036H36V42H30V6H54V36Z'%20fill='%23B7B1B1'/%3e%3cpath%20d='M84%2024V30H66V24H84Z'%20fill='%234B4646'/%3e%3cpath%20d='M84%2024H66V30H84V36H60V6H84V24ZM66%2018H78V12H66V18Z'%20fill='%23B7B1B1'/%3e%3cpath%20d='M108%2036H96V18H108V36Z'%20fill='%234B4646'/%3e%3cpath%20d='M108%2012H96V36H90V6H108V12ZM114%2036H108V12H114V36Z'%20fill='%23B7B1B1'/%3e%3cpath%20d='M144%2030H126V18H144V30Z'%20fill='%234B4646'/%3e%3cpath%20d='M144%2012H126V30H144V36H120V6H144V12Z'%20fill='%23F1ECEC'/%3e%3cpath%20d='M168%2030H156V18H168V30Z'%20fill='%234B4646'/%3e%3cpath%20d='M168%2012H156V30H168V12ZM174%2036H150V6H174V36Z'%20fill='%23F1ECEC'/%3e%3cpath%20d='M198%2030H186V18H198V30Z'%20fill='%234B4646'/%3e%3cpath%20d='M198%2012H186V30H198V12ZM204%2036H180V6H198V0H204V36Z'%20fill='%23F1ECEC'/%3e%3cpath%20d='M234%2024V30H216V24H234Z'%20fill='%234B4646'/%3e%3cpath%20d='M216%2012V18H228V12H216ZM234%2024H216V30H234V36H210V6H234V24Z'%20fill='%23F1ECEC'/%3e%3c/svg%3e)](/)

-   [GitHub](https://github.com/anomalyco/opencode)
-   [Docs](/docs)
-   [Data](/data)
-   [Zen](/zen)
-   [Go](/go)
-   [Enterprise](/enterprise)
-   [Download](/download)

Open menu

New

Desktop app available in beta on macOS, Windows, and Linux.[Download now](/download)[Download the desktop beta now](/download)

# The open source AI coding agent

Free models included or connect any model from any provider, including Claude, GPT, Gemini and more.

curlnpmbunbrewparu

curl -fsSL https://opencode.ai/install | bash

Your browser does not support the video tag.

### What is OpenCode?

OpenCode is an open source agent that helps you write code in your terminal, IDE, or desktop.

-   \[\*\]
    
    **LSP enabled** Automatically loads the right LSPs for the LLM
    
-   \[\*\]
    
    **Multi-session** Start multiple agents in parallel on the same project
    
-   \[\*\]
    
    **Share links** Share a link to any session for reference or to debug
    
-   \[\*\]
    
    **GitHub Copilot** Log in with GitHub to use your Copilot account
    
-   \[\*\]
    
    **ChatGPT Plus/Pro** Log in with OpenAI to use your ChatGPT Plus or Pro account
    
-   \[\*\]
    
    **Any model** 75+ LLM providers through Models.dev, including local models
    
-   \[\*\]
    
    **Any editor** Available as a terminal interface, desktop app, and IDE extension
    

[Read docs](/docs)

### The open source AI coding agent

\[\*\]

With over **160,000** GitHub stars, **900** contributors, and over **13,000** commits, OpenCode is used and trusted by over **7.5M** developers every month.

Fig 1.

**160K** GitHub Stars

Fig 2.

**900** Contributors

Fig 3.

**7.5M** Monthly Devs

### Built for privacy first

\[\*\]

OpenCode does not store any of your code or context data, so that it can operate in privacy sensitive environments. Learn more about [privacy](/docs/enterprise/).

### FAQ

-   What is OpenCode?
    
-   How do I use OpenCode?
    
-   Do I need extra AI subscriptions to use OpenCode?
    
-   Can I use my existing AI subscriptions with OpenCode?
    
-   Can I only use OpenCode in the terminal?
    
-   How much does OpenCode cost?
    
-   What about data and privacy?
    
-   Is OpenCode open source?
    

**Access reliable optimized models for coding agents**

Zen gives you access to a handpicked set of AI models that OpenCode has tested and benchmarked specifically for coding agents. No need to worry about inconsistent performance and quality across providers, use validated models that work.

[Learn about Zen](/zen)

### Be the first to know when we release new products

Join the waitlist for early access.

Subscribe

[GitHub \[160K\]](https://github.com/anomalyco/opencode)

[Docs](/docs)

[Changelog](/changelog)

[Discord](/discord)

[X](https://x.com/opencode)

©2026 [Anomaly](https://anoma.ly)[Brand](/brand)[Privacy](/legal/privacy-policy)[Terms](/legal/terms-of-service)

English
```

**Tool: websearch**

**Input:**
```json
{
  "query": "opencode AI coding agent architecture CLI tool features 2026"
}
```

**Output:**
```
Title: anomalyco/opencode
URL: https://github.com/anomalyco/opencode/?tab=readme-ov-file
Published: 2025-04-30T20:08:00.000Z
Author: N/A
Highlights:
The open source coding agent.
...
- Stars: 176213
- Forks: 21453
- Watchers: 682
- Open issues: 7218
- Primary language: TypeScript
- Languages: TypeScript (68.9%), MDX (27.4%), CSS (3.1%), HTML (0.2%), JavaScript (0.1%), Astro (0.1%), Shell, Nix, Dockerfile, PowerShell
- License: MIT License (MIT)
- Default branch: dev
- Homepage: https://opencode.ai
- Created: 2025-04-30T20:08:00Z
- Last push: 2026-06-19T08:28:08Z
- Contributors: 460 (top: thdxr, adamdotdevin, rekram1-node, opencode-agent[bot], kitlangton, actions-user, iamdavidhill, fwang, jayair, Brendonovich)
- Releases: 825
- Latest release: v1.17.8 (2026-06-17T21:27:18Z)
...
```bash
# YOLO
curl -fsSL https://opencode.ai/install | bash
...
# Package managers
npm i -g opencode-ai@latest        # or bun/pnpm/yarn
scoop install opencode             # Windows
choco install opencode             # Windows
brew install anomalyco/tap/opencode # macOS and Linux (recommended, always up to date)
brew install opencode              # macOS and Linux (official brew formula, updated less)
sudo pacman -S opencode            # Arch Linux (Stable)
paru -S opencode-bin               # Arch Linux (Latest from AUR)
mise use -g opencode               # Any OS
nix run nixpkgs#opencode           # or github:anomalyco/opencode for latest dev branch
```
...
### Desktop App (BETA)
...
OpenCode is also available as a desktop application. Download directly from the [releases page](https://github.com/anomalyco/opencode/releases) or [opencode.ai/download](https://opencode.ai/download).
...
| Platform | Download |
| --- | --- |
| macOS (Apple Silicon) | `opencode-desktop-mac-arm64.dmg` |
| macOS (Intel) | `opencode-desktop-mac-x64.dmg` |
| Windows | `opencode-desktop-windows-x64.exe` |
| Linux | `.deb`, `.rpm`, or `.AppImage` |
...
#### Installation Directory
...
The install script respects the following
...
order for the installation path:
...
OPENCODE_INSTALL_DIR` - Custom installation directory
...
XDG_
...
_DIR` - XDG
...
Directory Specification compliant path
...
(if it
...
or can be
...
` - Default
...
OpenCode includes two built-in agents you can switch between with the `Tab` key.
...
- **build** - Default, full-access agent for development work
- **plan** - Read-only agent for analysis and code exploration

- Denies file edits by default
 - Asks permission before running bash commands
 - Ideal for exploring unfamiliar codebases or planning changes
...
Also included is a **general** subagent for complex searches and multistep tasks.
This is used internally and can be invoked using `@general` in messages.
...
Learn more about [agents](https://opencode.ai/docs/agents).
...
For more info on how to configure OpenCode, [**head over to our docs**](https://opencode.ai/docs).

---

Title: OpenCode | The open source AI coding agent
URL: https://opencode.ai/
Published: N/A
Author: N/A
Highlights:
OpenCode | The open source AI coding agent

New

Desktop app available in beta on macOS, Windows, and Linux. Download now Download the desktop beta now

# The open source AI coding agent

Free models included or connect any model from any provider, including Claude, GPT, Gemini and more.

curlnpmbunbrewparu

```
curl -fsSL https://opencode.ai/install | bash
```

Your browser does not support the video tag.

### What is OpenCode?

OpenCode is an open source agent that helps you write code in your terminal, IDE, or desktop.

[*]

LSP enabled Automatically loads the right LSPs for the LLM

[*]

Multi-session Start multiple agents in parallel on the same project

[*]

Share links Share a link to any session for reference or to debug

[*]

GitHub Copilot Log in with GitHub to use your Copilot account

[*]

ChatGPT Plus/Pro Log in with OpenAI to use your ChatGPT Plus or Pro account

[*]

Any model 75+ LLM providers through Models.dev, including local models

[*]

Any editor Available as a terminal interface, desktop app, and IDE extension

Read docs

### The open source AI coding agent

[*]

With over 160,000 GitHub stars, 900 contributors, and over 13,000 commits, OpenCode is used and trusted by over 7.5M developers every month.

Fig 1. 160K GitHub Stars

Fig 2. 900 Contributors

Fig 3. 7.5M Monthly Devs

### Built for privacy first

[*]

OpenCode does not store any of your code or context data, so that it can operate in privacy sensitive environments. Learn more about privacy.

### FAQ

What is OpenCode?

How do I use OpenCode?

Do I need extra AI subscriptions to use OpenCode?

Can I use my existing AI subscriptions with OpenCode?

Can I only use OpenCode in the terminal?

How much does OpenCode cost?

What about data and privacy?

Is OpenCode open source?

Access reliable optimized models for coding agents

Zen gives you access to a handpicked set of AI models that OpenCode has tested and benchmarked specifically for coding agents. No need to worry about inconsistent performance and quality across providers, use validated models that work.

Learn about Zen

### Be the first to know when we release new products

Join the waitlist for early access.

Subscribe

English

---

Title: Dissecting OpenCode: A Complete Architecture Analysis of an Open-Source AI Coding Agent
URL: https://zengineer.blog/blog/tech/opencode-architecture-deep-dive-en/
Published: 2026-04-09T14:18:27.000Z
Author: N/A
Highlights:
OpenCode is an open-source AI Coding Agent that offers three interfaces: CLI/TUI, Web, and Desktop. Its source code is an excellent resource for learning "how to build a production-grade AI Agent system from scratch." This article, based on deep reading of OpenCode's source code, dissects each layer of its architecture to show what a mature AI Coding Agent looks like on the inside.
...
All important logic lives in`packages/opencode/src/`. This package itself is a micro operating system — with its own Agent scheduler, event bus, permission system, storage layer, and HTTP Server.
...
There's a key architectural decision here: TUI and Server run in different threads. The Worker Thread handles all I/O-intensive work (LLM streaming, file operations, MCP connections), while the TUI main thread only handles rendering and user input. They communicate via RPC, and events are forwarded from Worker to TUI through GlobalBus.
...
The core difference between each Agent isn't the prompt — it's the Permission Ruleset, which determines which tools the Agent can use. The clever part about the`plan` Agent: it doesn't rely on a prompt telling the LLM "don't modify files" — it simply removes write tools from the available list. Tools the LLM can't see, it can't call.
...
Agents can delegate to each other through the`task` tool. When the`build` Agent needs to search through a lot of code, it can spawn an`explore` sub-agent to execute in a separate Session, then bring the results back. This delegation is recursive — sub-agents can also delegate further, but each layer is constrained by its own Permission Ruleset.
...
Tools are the only interface between the Agent and the external world. OpenCode's Tool abstraction is elegantly designed:
...
Each tool is lazily initialized —`init()` is only called on first use, so startup speed isn't affected by the number of tools. The`metadata` callback mechanism allows tools to update the UI in real-time during execution (e.g., the`bash` tool streams command execution progress), rather than only reporting back when complete.
...
Core file operations:`bash`,`read`,`write`,`edit`,`apply_patch`
...
Search and exploration:`glob`,`grep`,`websearch`,`codesearch`,`webfetch`
...
Agent collaboration:`task`(delegate sub-agent),`question`(ask user),`skill`(load commands)
...
Batch and management:`batch`(execute up to 25 tools in parallel),`todowrite`,`lsp`
...
The`edit` tool is the most sophisticated part of the Tool system. When LLMs specify code to replace, there are often tiny deviations — an extra space, missing indentation, inconsistent escape characters. OpenCode uses 9 different replacers in sequence to ensure it finds the correct match position as much as possible:

---

Title: Agents | OpenCode
URL: https://opencode.ai/docs/agents/
Published: N/A
Author: N/A
Highlights:
There are two types of agents in OpenCode; primary agents and subagents.
...
Primary agents are the main assistants you interact with directly. You can cycle through them using the Tab key, or your configured `switch_agent` keybind. These agents handle your main conversation. Tool access is configured via permissions — for example, Build has all tools enabled while Plan is restricted.
...
Subagents are specialized assistants that primary agents can invoke for specific tasks. You can also manually invoke them by @ mentioning them in your messages.
...
OpenCode comes with two built-in primary agents and three built-in subagents.
...
Build is the default primary agent with all tools enabled. This is the standard agent for development work where you need full access to file operations and system commands.
...
A restricted agent designed for planning and analysis. We use a permission system to give you more control and prevent unintended changes.
...
This agent is useful when you want the LLM to analyze code, suggest changes, or create plans without making any actual modifications to your codebase.
...
A general-purpose agent for researching complex questions and executing multi-step tasks. Has full tool access (except todo), so it can make file changes when needed. Use this to run multiple units of work in parallel.
...
A fast, read-only agent for exploring codebases. Cannot modify files. Use this when you need to quickly find files by patterns, search code for keywords, or answer questions about the codebase.
...
A read-only agent for external docs and dependency research. Use this when you need to clone a dependency repository into OpenCode's managed cache, inspect library source, or cross-reference local code against upstream implementations without modifying your workspace.
...
You can customize the built-in agents or create your own through configuration. Agents can be configured in two ways:
...
Configure agents in your `opencode.json` config file:
...
You can also define agents using markdown files. Place them in:
...
. Useful for using different models optimized for different
...
. For example
...
### Tools (deprecated)
...
You can configure permissions to manage what actions an agent can take. Each permission key can be set to:
...
- Build agent: Full development work with all tools enabled
- Plan agent: Analysis and planning without making changes
- Review agent: Code review with read-only access plus documentation tools
- Debug agent: Focused on investigation with bash and read tools enabled
- Docs agent: Documentation writing with file operations but no system commands

---

Title: CLI | OpenCode
URL: https://opencode.ai/docs/cli/
Published: N/A
Author: N/A
Highlights:
The OpenCode CLI by default starts the TUI when run without any arguments.
...
But it also accepts commands as documented on this page. This allows you to interact with OpenCode programmatically.
...
### tui
...
| Short | Description |
...
| --- | --- | --- |
...
last session |
...
use with `--continue
...
`--session`) |
...
use in the form of provider/model |
...
The OpenCode CLI also has the following commands.
...
Manage agents for OpenCode.
...
Create a new agent with custom configuration.
...
This command will guide you through creating a new agent with a custom system prompt and permission configuration. Anything you don't allow is denied in the generated agent's frontmatter.
...
| Flag | Short | Description |
| --- | --- | --- |
| `{"--path"}` | | Directory to write the agent file to (defaults to global or `.opencode/agent` based on the prompt) |
| `{"--description"}` | | What the agent should do |
| `{"--mode"}` | | Agent mode: `all`, `primary`, or `subagent` |
| `{"--permissions"}` | | Comma-separated list of permissions to allow (default: all). Available: `bash`, `read`, `edit`, `glob`, `grep`, `webfetch`, `task`, `todowrite`, `websearch`, `lsp`, `skill`. Anything omitted is denied. Alias: `--tools` |
| `{"--model"}` | `-m` | Model to use, in `provider/model` format |
...
Passing all of `--path`, `--description`, `--mode`, and `--permissions` runs the command non-interactively.
...
Attach a terminal to an already running OpenCode backend server started via `serve` or `web` commands.
...
OpenCode is powered by the provider list at Models.dev, so you can use `opencode auth login` to configure API keys for any provider you'd like to use. This is stored in `~/.local/share/opencode/auth.json`.
...
### mcp
...
Run opencode in non-interactive mode by passing a prompt directly.
...
This is useful for scripting, automation, or when you want a quick answer without launching the full TUI. For example.
...
You can also attach to a running `opencode serve` instance to avoid
...
server cold boot times on every run:
...
This starts an HTTP server that provides API access to opencode functionality without the TUI interface. Set `OPENCODE_SERVER_PASSWORD` to enable HTTP basic auth (username defaults to `opencode`).
...
to enable HTTP
...
### acp
...
## Global Flags
...
## Environment variables
...
| `OPENCODE_EXPERIMENTAL_BACKGROUND
...
| `OPENCODE_EXPERIMENTAL
...
| `OPENCODE_EXPERIMENTAL_SCOUT` | boolean | Enable
...
subagent |
...
| `OPENCODE_EXPERIMENTAL

---

Title: Architecture Overview | sst/opencode | DeepWiki
URL: https://deepwiki.com/sst/opencode/1.2-architecture-overview
Published: 2026-05-09T00:00:00.000Z
Author: N/A
Highlights:
This document presents the high-level system architecture of OpenCode, describing how its major components interact to deliver AI-powered coding assistance. It covers the session processing pipeline, provider integration, and the client-server communication model.
...
OpenCode is built on a layered architecture that bridges high-level user intent with low-level system operations (file manipulation, terminal execution, and LSP interactions) using the [Effect](https://effect.website/) ecosystem for robust service management and dependency injection.
...
OpenCode follows a layered architecture where client applications communicate with an HTTP server that orchestrates AI sessions, provider interactions, and tool executions. The system uses an [Effect](https://effect.website/) based backend that supports both a public API and a internal instance management.
...
3. **Prompt Orchestration**: The `SessionPrompt.Service` handles incoming prompts, resolving them into `MessageV2` structures and managing the agentic loop [packages/opencode/src/session/prompt.ts84-93](https://github.com/sst/opencode/blob/47f33329/packages/opencode/src/session/prompt.ts#L84-L93)
...
4. **LLM Execution**: The `LLM.Service` manages streaming interactions. It prepares requests via `LLMRequestPrep` and uses `LLMClient` for routing to providers [packages/opencode/src/session/llm.ts71-81](https://github.com/sst/opencode/blob/47f33329/packages/opencode/src/session/llm.ts#L71-L81) [packages/opencode/src/session/llm.ts106-113](https://github.com/sst/opencode/blob/47f33329/packages/opencode/src/session/llm.ts#L106-L113)
...
The session pipeline transforms user prompts into assistant actions through an agentic loop (`SessionPrompt.loop`), managing context overflow via compaction and ensuring persistence through a specialized processor.
...
/compaction.ts42-77](https://github.com/sst/op
...
/blob/47f33329/packages/opencode/src/
...
/compaction.ts#L42-L77)[packages/opencode/src/session/compaction.ts186-206](https://github
...
com/sst/opencode/blob/47f33329/packages/
...
encode/src/
...
|`LLM.Service`|Abstraction layer that prepares `LLMRequest` and handles provider-specific streaming (e.g., GitLab Workflow).|[packages/opencode/src/session/llm.ts52-54](https://github.com/sst/opencode/blob/47f33329/packages/opencode/src/session/llm.ts#L52-L54)[packages/opencode/src/session/llm.ts118-125](https://github.com/sst/opencode/blob/47f33329/packages/opencode/src/session/llm.ts#L118-
...
OpenCode integrates with various LLM providers by leveraging a custom transformation layer and model metadata resolution.
...
OpenCode uses a SQLite database with [Drizzle ORM](https://orm.drizzle.team/) for persistent storage and an event-based system for real-time updates.

---

Title: Core Application | anomalyco/opencode | DeepWiki
URL: https://deepwiki.com/anomalyco/opencode/2-core-application
Published: 2026-06-14T11:27:16.000Z
Author: N/A
Highlights:
The Core Application is the main OpenCode server package ([packages/opencode](https://github.com/anomalyco/opencode/blob/7ad68f81/packages/opencode)) that provides the foundational AI agent capabilities. It implements an Effect-based server with an embedded CLI interface, managing AI conversations (sessions), tool execution, provider integrations, and real-time event streaming. The server can run in-process (local mode) or as a networked service (remote mode), exposing an OpenAPI-compliant REST API.
...
The Core Application follows a layered architecture organized via the **Effect** library to model side effects and async services. It cleanly separates layers such as transport (HTTP/stdio/internal RPC), business logic (sessions, agents, projects), and execution (tools, permissions, shells).
...
* Multiple transport modes: CLI, REST API, internal RPC, and ACP (Agent Client Protocol
...
tools with permissions
...
The Core Application boots via the main CLI entrypoint (`packages/opencode/src/index.ts`). It parses commands using `yargs`, sets environment flags, initializes the heap snapshot system, and delegates execution to the appropriate command handler.
...
The CLI provides a rich set of commands accessed via `opencode <command>`. The commands include:
...
|Command|Description|Key File Location|
...
|`run`|Runs AI agent tasks with optional project|`cli/cmd/run.ts`|
...
|`serve`|Starts a headless HTTP server|`cli/cmd/serve.ts`|
...
|`web`|Runs server and opens the web client|`cli/cmd/web.ts`|
...
|`acp`|Starts the Agent Client Protocol server|`cli/cmd/acp.ts`|
...
|`tui` (default)|Starts the Terminal User Interface (TUI)|`cli/cmd/tui/thread.ts`|
...
|`agent`|Manage agent definitions|`cli/cmd/agent.ts`|
...
|`models`|List or configure AI models|`cli/cmd/models.ts`|
|`providers`|List or configure AI providers|`cli/cmd/providers.ts`|
...
|`session`|Manage AI chat sessions|`cli/cmd/session.ts`|
...
|`plugin`|Manage plugins|`cli/cmd/plug.ts`|
...
|`stats`|Collect and show server statistics|`cli/cmd/stats.ts`|
...
|`upgrade`/`uninstall`|Upgrade or uninstall CLI|`cli/cmd/upgrade.ts`, `cli/cmd/uninstall.ts`|
...
The core runtime includes a session management system that tracks conversation state, manages message parts, and interacts with AI agents.
...
## Tool System & Permissions
...
Tool execution is a key feature, enabling agents to run commands like `bash`, `edit`, `read`, `write`, `grep`, and custom tasks. The Core Application:
...
editors and web clients.
...
* HTTP REST API for external clients
...
* Internal RPC between the CLI main thread and the TUI worker process
...
* JSON-RPC over stdio via ACP protocol for IDEs like Zed

---

Title: OpenCode Deep Dive: Provider-Agnostic AI CLI in 2026 (v1.3.3 Update) |
Sanj
URL: https://sanj.dev/post/opencode-deep-dive-2026/
Published: 2026-03-24T16:00:00.000Z
Author: Sanj
Highlights:
The honeymoon phase with model-locked AI coding agents is officially over. While Claude Code and Gemini CLI offer incredible reasoning out of the box,
...
Since its explosion in popularity last year, OpenCode has evolved from a simple wrapper into a sophisticated, multi-agent orchestration platform that supports over 75 LLM providers. I’ve been running OpenCode v1.3.0 (released just this week) across local monorepos and distributed teams, and there are three core reasons why it’s becoming the default choice for engineers who value unlocked flexibility.
...
about redundancy.
...
While Aider and Claude Code rely on a standard terminal chat interface, OpenCode’s Terminal User Interface (TUI) is a legitimate “Mission Control” for your codebase. It doesn’t just scroll text; it organizes your tasks visually.
...
One of the standout features in the latest v1.3.0 release is the Git-backed Session Review. Instead of having to`git status` in a separate terminal to see what the agent actually changed, the TUI provides a visual diff and status map directly in the session. You can see which files are being analyzed, which are being edited, and most importantly, why the agent made a specific decision through its transparent planning mode.
...
The “Plan” agent (`Tab` to toggle) is particularly useful for complex architectural changes. It performs read-only analysis of your repository, identifies cross-file dependencies, and presents a multi-step execution plan before you ever authorize a single write. It’s the difference between blindly trusting an AI to refactor your auth layer and having an expert peer walk you through the logic first.
...
OpenCode’s real power comes from its dual-agent architecture separating intention from execution. You can toggle between the Plan agent for architectural strategy and fact-finding, and the Build agent to execute those changes. By separating these concerns, you get the context-awareness of a senior engineer without risking accidental overwrites during the brainstorming phase.
...
Managing long-running sessions has always been a token-burning nightmare, but OpenCode’s Auto Compact feature solves this brilliantly. As your session grows, OpenCode intelligently summarizes the conversation history and architectural findings, compacting the context window without losing the core “memory” of the task. This keeps latency low and costs predictable even when you’re working on a three-day refactoring project.
...
While OpenCode initially made waves by running exclusively on Bun, v1.3.0 introduces full Node.js support. You can now run the tool using a dedicated Node.js entry point, resolving adoption blockers for teams with strict corporate runtime policies.
```

---

## Assistant (Plan · DeepSeek V4 Flash Free · 28.5s)

_Thinking:_

Now I have a comprehensive understanding of opencode's architecture. It's a TypeScript-based AI coding agent with:
- Agent system (build/plan agents with different permission levels)
- Tool system (bash, read, write, edit, grep, glob, etc.)
- Multi-provider LLM support (75+ providers)
- Session management
- SQLite persistence
- Event/streaming architecture
- HTTP API, CLI, TUI interfaces

The user wants something like opencode but integrated into their TaskWatch-like app. So basically a Python-based task timer/manager with an integrated AI coding agent.

Let me now formulate the complete plan.

Key architecture decisions:
1. **Python** - user confirmed
2. **AI agent like opencode** - autonomous agent with tool use, task execution
3. **Waybar integration** - Unix socket IPC for real-time state updates
4. **Separate daemon + CLI** architecture

Let me think about how to structure this properly:

**Core Components:**

1. **`taskwatchd` - Background Daemon**
   - Manages timer state (pomodoro sessions)
   - Task database (SQLite)
   - Unix socket for IPC
   - AI agent orchestrator
   - Periodically writes state file for Waybar

2. **`taskwatch` - CLI Client**
   - `taskwatch start/stop/pause` - timer control
   - `taskwatch task add/list/done` - task management
   - `taskwatch agent "prompt"` - interact with AI agent
   - `taskwatch waybar` - output JSON for Waybar

3. **Waybar Integration**
   - Daemon writes to `/tmp/taskwatch-waybar.json` or provides via socket
   - Waybar `custom/taskwatch` module reads it

4. **AI Agent System**
   - Tool-based agent similar to opencode
   - Tools: bash, read, write, edit, glob, grep, websearch, webfetch
   - Multiple LLM backends: Ollama (local), OpenAI, Anthropic
   - Agent can pick tasks from the task list and work on them
   - Structured output for task status updates

Let me design the plan more concretely:

```
taskwatch/
├── taskwatch/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py          # CLI entry point (click/typer)
│   │   ├── timer_cmd.py     # timer commands
│   │   ├── task_cmd.py      # task commands
│   │   ├── agent_cmd.py     # agent commands
│   │   └── waybar_cmd.py    # waybar output
│   ├── daemon/
│   │   ├── __init__.py
│   │   ├── server.py        # Unix socket server
│   │   └── main.py          # Daemon entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── timer.py         # Pomodoro timer engine
│   │   ├── tasks.py         # Task model + storage
│   │   ├── storage.py       # SQLite backend
│   │   └── settings.py      # Configuration
│   └── agent/
│       ├── __init__.py
│       ├── engine.py        # Agent loop (LLM + tools)
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── bash.py      # Run shell commands
│       │   ├── read_file.py # Read files
│       │   ├── write_file.py# Write files
│       │   ├── edit_file.py # Edit files
│       │   ├── glob.py      # File search
│       │   ├── grep.py      # Content search
│       │   ├── websearch.py # Web search
│       │   ├── task_ops.py  # Task list operations
│       │   └── timer_ops.py # Timer control
│       └── llm/
│           ├── __init__.py
│           ├── base.py      # LLM interface
│           ├── ollama.py    # Ollama backend
│           ├── openai.py    # OpenAI backend
│           └── anthropic.py # Anthropic backend
├── scripts/
│   └── taskwatch-waybar.sh  # Waybar helper script
├── pyproject.toml
└── README.md
```

Now let me present the plan to the user.

Here's the plan for **taskwatch** — a Python-based task timer with AI coding agent and Waybar integration, inspired by opencode's architecture.

---

## Architecture Overview

```
┌─────────────────┐     Unix Socket     ┌──────────────┐
│   taskwatch CLI  │◄──────────────────►│  taskwatchd   │
│  (typer/click)   │                     │  (daemon)     │
└─────────────────┘                     │              │
                                        │  ┌─────────┐ │
┌─────────────────┐     State File      │  │  Timer   │ │
│   Waybar         │◄───────────────────│  │  Engine  │ │
│  custom/taskwatch│   /tmp/taskwatch-  │  ├─────────┤ │
│                  │   waybar.json      │  │  Tasks   │ │
└─────────────────┘                     │  │  (SQLite)│ │
                                        │  ├─────────┤ │
┌─────────────────┐                     │  │  Agent   │ │
│   Terminal/TUI   │◄───────────────────│  │  Engine  │ │
│                  │     CLI commands   │  └─────────┘ │
└─────────────────┘                     └──────────────┘
```

## Component Breakdown

### 1. Core (`taskwatch.core`)
- **Timer engine** — Pomodoro with adaptive durations, focus/break/long-break cycles
- **Task model** — title, description, priority, deadline, status, tags, estimated pomodoros
- **Storage** — SQLite via SQLAlchemy or aiosqlite
- **Settings** — YAML config (`~/.config/taskwatch/config.yml`)

### 2. Daemon (`taskwatchd`)
- Background Unix socket server (asyncio-based)
- Manages timer state, task CRUD, and agent lifecycle
- Writes Waybar-compatible JSON to `/tmp/taskwatch-waybar.json` on state changes
- CLI commands proxy through the socket to the daemon

### 3. CLI (`taskwatch`)
```
taskwatch timer start [25m]     # Start a focus session
taskwatch timer pause            # Pause current timer
taskwatch timer resume           # Resume paused timer
taskwatch timer cancel           # Cancel current session
taskwatch timer status           # Show current timer state

taskwatch task add "title" -p high -d "details"
taskwatch task list              # List tasks (by status/priority)
taskwatch task done <id>         # Mark task complete
taskwatch task start <id>        # Start timer for specific task
taskwatch task suggest           # AI suggests what to work on

taskwatch waybar                 # Print JSON for Waybar (used in exec)

taskwatch agent "do something"   # Run AI agent with a prompt
taskwatch agent run-task <id>    # AI agent executes a specific task
taskwatch agent status           # Check agent progress

taskwatch daemon start|stop|status
```

### 4. Waybar Integration
Example Waybar config:
```json
"custom/taskwatch": {
    "exec": "taskwatch waybar",
    "exec-on-event": false,
    "return-type": "json",
    "format": "{icon} {}",
    "format-icons": { "focus": "🍅", "break": "☕", "standby": "⏸", "paused": "⏸" },
    "on-click": "taskwatch timer toggle",
    "on-click-right": "taskwatch timer new 25"
}
```
The daemon writes a state file that `taskwatch waybar` reads. The file updates on every second/tick via `inotify` or polling.

### 5. AI Agent (`taskwatch.agent`) — *like opencode*
**Engine:**
- Agentic loop: LLM → decides tool → executes → observes → LLM
- Session-based with conversation history
- Permission system (tools the agent can use)

**LLM backends (pluggable):**
| Backend | Config |
|---------|--------|
| Ollama | Local, e.g. `llama3`, `mistral`, `codellama` |
| OpenAI | `gpt-4o` with API key |
| Anthropic | `claude-sonnet-4` with API key |
| OpenCode-compatible | Any opencode-supported model via its API |

**Tools the agent can use:**
| Tool | Description |
|------|-------------|
| `bash` | Run shell commands |
| `read` | Read files |
| `write` | Write files |
| `edit` | Edit files (like opencode's smart edit) |
| `glob` | Find files by pattern |
| `grep` | Search file contents |
| `websearch` | Search the web |
| `webfetch` | Fetch URLs |
| `taskops` | Create/update/complete tasks |
| `timerctl` | Control the timer |

**Agent capabilities:**
- Autonomous task execution: "Fix the bug in src/main.py and mark the task done"
- Task suggestions: "What should I work on next?" (reads task list, prioritizes)
- Smart work sessions: AI sets Pomodoro duration based on task complexity
- Productivity summaries: "What did I accomplish this week?"

### 6. TUI (optional, stretch goal)
- Textual (Python TUI framework) or Rich-based
- Shows task list, timer status, agent conversation
- Runs as `taskwatch tui`

---

## Project File Tree
```
taskwatch/
├── taskwatch/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── app.py            # Main CLI app (typer)
│   │   ├── timer.py
│   │   ├── task.py
│   │   ├── agent.py
│   │   ├── daemon.py
│   │   └── waybar.py
│   ├── daemon/
│   │   ├── __init__.py
│   │   ├── server.py         # Unix socket server
│   │   └── client.py         # Socket client for CLI
│   ├── core/
│   │   ├── __init__.py
│   │   ├── timer.py
│   │   ├── task.py
│   │   ├── storage.py        # SQLite
│   │   └── config.py
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── engine.py         # Agentic loop
│   │   ├── session.py        # Conversation state
│   │   ├── permissions.py    # Tool permission rules
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── bash.py
│   │   │   ├── read.py
│   │   │   ├── write.py
│   │   │   ├── edit.py
│   │   │   ├── glob.py
│   │   │   ├── grep.py
│   │   │   ├── websearch.py
│   │   │   ├── webfetch.py
│   │   │   ├── taskops.py
│   │   │   └── timerctl.py
│   │   └── llm/
│   │       ├── __init__.py
│   │       ├── base.py
│   │       ├── ollama.py
│   │       ├── openai.py
│   │       └── anthropic.py
│   └── tui/                  # Optional
│       └── app.py
├── scripts/
│   └── install-service.sh    # systemd user service for daemon
├── pyproject.toml
└── README.md
```

## Implementation Order

| Phase | What | Why first |
|-------|------|-----------|
| **1** | Core: timer engine, task model, SQLite storage | Foundation — everything depends on these |
| **2** | Daemon: socket server + client | Need IPC before CLI/Waybar can work |
| **3** | CLI: timer + task commands | Core user interaction |
| **4** | Waybar: state file writer + JSON output | Your main integration goal |
| **5** | Agent: LLM interface + tool system + agentic loop | The opencode-like agent |
| **6** | Agent tools: taskops, timerctl, file ops | Agent can interact with tasks and the system |
| **7** | TUI (optional) | Nice-to-have terminal interface |

## Key Dependencies
- **typer** — CLI framework
- **asyncio** — async daemon + socket IPC  
- **aiosqlite** / **sqlite3** — persistence
- **httpx** — LLM API calls, web fetch
- **ollama** / **openai** / **anthropic** SDKs
- **pyyaml** — config files
- **rich** — CLI output formatting (and TUI if built)

---

## Questions for you:

1. **Daemon auto-start** — Should the daemon launch automatically when you run any `taskwatch` command (like Docker), or do you prefer a separate `taskwatch daemon start`?
2. **Agent model default** — What's your primary LLM setup? Ollama with which model, or do you have OpenAI/Anthropic API keys?
3. **TUI priority** — Do you want a Textual TUI (like opencode's) now, or is CLI + Waybar sufficient for v1?

---

