function(packageName_target_warnings target)
  if(MSVC)
    target_compile_options(${target} PRIVATE /W4 /permissive- /utf-8
      $<$<BOOL:${packageName_WARNINGS_AS_ERRORS}>:/WX>)
  else()
    target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Wconversion -Wshadow
      $<$<BOOL:${packageName_WARNINGS_AS_ERRORS}>:-Werror>)
  endif()
endfunction()
