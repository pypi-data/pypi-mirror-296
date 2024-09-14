async function V() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function Z(e) {
  return await V(), e().then((t) => t.default);
}
function O(e) {
  const {
    gradio: t,
    _internal: o,
    ...s
  } = e;
  return Object.keys(o).reduce((i, n) => {
    const l = n.match(/bind_(.+)_event/);
    if (l) {
      const a = l[1], r = a.split("_"), _ = (...f) => {
        const d = f.map((u) => f && typeof u == "object" && (u.nativeEvent || u instanceof Event) ? {
          type: u.type,
          detail: u.detail,
          timestamp: u.timeStamp,
          clientX: u.clientX,
          clientY: u.clientY,
          targetId: u.target.id,
          targetClassName: u.target.className,
          altKey: u.altKey,
          ctrlKey: u.ctrlKey,
          shiftKey: u.shiftKey,
          metaKey: u.metaKey
        } : u);
        return t.dispatch(a.replace(/[A-Z]/g, (u) => "_" + u.toLowerCase()), {
          payload: d,
          component: s
        });
      };
      if (r.length > 1) {
        let f = {
          ...s.props[r[0]] || {}
        };
        i[r[0]] = f;
        for (let u = 1; u < r.length - 1; u++) {
          const h = {
            ...s.props[r[u]] || {}
          };
          f[r[u]] = h, f = h;
        }
        const d = r[r.length - 1];
        return f[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = _, i;
      }
      const p = r[0];
      i[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = _;
    }
    return i;
  }, {});
}
function S() {
}
function B(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function G(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return S;
  }
  const o = e.subscribe(...t);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function y(e) {
  let t;
  return G(e, (o) => t = o)(), t;
}
const w = [];
function g(e, t = S) {
  let o;
  const s = /* @__PURE__ */ new Set();
  function i(a) {
    if (B(e, a) && (e = a, o)) {
      const r = !w.length;
      for (const _ of s)
        _[1](), w.push(_, e);
      if (r) {
        for (let _ = 0; _ < w.length; _ += 2)
          w[_][0](w[_ + 1]);
        w.length = 0;
      }
    }
  }
  function n(a) {
    i(a(e));
  }
  function l(a, r = S) {
    const _ = [a, r];
    return s.add(_), s.size === 1 && (o = t(i, n) || S), a(e), () => {
      s.delete(_), s.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: n,
    subscribe: l
  };
}
const {
  getContext: P,
  setContext: j
} = window.__gradio__svelte__internal, H = "$$ms-gr-antd-slots-key";
function J() {
  const e = g({});
  return j(H, e);
}
const Q = "$$ms-gr-antd-context-key";
function T(e) {
  var a;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = $(), o = ee({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((r) => {
    o.slotKey.set(r);
  }), W();
  const s = P(Q), i = ((a = y(s)) == null ? void 0 : a.as_item) || e.as_item, n = s ? i ? y(s)[i] : y(s) : {}, l = g({
    ...e,
    ...n
  });
  return s ? (s.subscribe((r) => {
    const {
      as_item: _
    } = y(l);
    _ && (r = r[_]), l.update((p) => ({
      ...p,
      ...r
    }));
  }), [l, (r) => {
    const _ = r.as_item ? y(s)[r.as_item] : y(s);
    return l.set({
      ...r,
      ..._
    });
  }]) : [l, (r) => {
    l.set(r);
  }];
}
const U = "$$ms-gr-antd-slot-key";
function W() {
  j(U, g(void 0));
}
function $() {
  return P(U);
}
const X = "$$ms-gr-antd-component-slot-context-key";
function ee({
  slot: e,
  index: t,
  subIndex: o
}) {
  return j(X, {
    slotKey: g(e),
    slotIndex: g(t),
    subSlotIndex: g(o)
  });
}
function ve() {
  return P(X);
}
function te(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Y = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function o() {
      for (var n = "", l = 0; l < arguments.length; l++) {
        var a = arguments[l];
        a && (n = i(n, s(a)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return o.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var l = "";
      for (var a in n)
        t.call(n, a) && n[a] && (l = i(l, a));
      return l;
    }
    function i(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    e.exports ? (o.default = o, e.exports = o) : window.classNames = o;
  })();
})(Y);
var ne = Y.exports;
const q = /* @__PURE__ */ te(ne), {
  getContext: se,
  setContext: xe
} = window.__gradio__svelte__internal, oe = "$$ms-gr-antd-iconfont-context-key";
function ie() {
  return se(oe);
}
const {
  SvelteComponent: le,
  assign: re,
  check_outros: ce,
  component_subscribe: K,
  create_component: ue,
  destroy_component: ae,
  detach: D,
  empty: F,
  flush: b,
  get_spread_object: A,
  get_spread_update: _e,
  group_outros: fe,
  handle_promise: me,
  init: de,
  insert: L,
  mount_component: be,
  noop: m,
  safe_not_equal: pe,
  transition_in: C,
  transition_out: I,
  update_await_block_branch: he
} = window.__gradio__svelte__internal;
function R(e) {
  let t, o, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: we,
    then: ye,
    catch: ge,
    value: 19,
    blocks: [, , ,]
  };
  return me(
    /*AwaitedIcon*/
    e[3],
    s
  ), {
    c() {
      t = F(), s.block.c();
    },
    m(i, n) {
      L(i, t, n), s.block.m(i, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, o = !0;
    },
    p(i, n) {
      e = i, he(s, e, n);
    },
    i(i) {
      o || (C(s.block), o = !0);
    },
    o(i) {
      for (let n = 0; n < 3; n += 1) {
        const l = s.blocks[n];
        I(l);
      }
      o = !1;
    },
    d(i) {
      i && D(t), s.block.d(i), s.token = null, s = null;
    }
  };
}
function ge(e) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function ye(e) {
  let t, o;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[0].elem_style
      )
    },
    {
      className: q(
        /*$mergedProps*/
        e[0].elem_classes,
        "ms-gr-antd-icon"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[0].elem_id
      )
    },
    /*$mergedProps*/
    e[0].props,
    O(
      /*$mergedProps*/
      e[0]
    ),
    {
      slots: (
        /*$slots*/
        e[1]
      )
    },
    {
      name: (
        /*$mergedProps*/
        e[0].value
      )
    },
    {
      Iconfont: (
        /*$Iconfont*/
        e[2]
      )
    }
  ];
  let i = {};
  for (let n = 0; n < s.length; n += 1)
    i = re(i, s[n]);
  return t = new /*Icon*/
  e[19]({
    props: i
  }), {
    c() {
      ue(t.$$.fragment);
    },
    m(n, l) {
      be(t, n, l), o = !0;
    },
    p(n, l) {
      const a = l & /*$mergedProps, $slots, $Iconfont*/
      7 ? _e(s, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          n[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: q(
          /*$mergedProps*/
          n[0].elem_classes,
          "ms-gr-antd-icon"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          n[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && A(
        /*$mergedProps*/
        n[0].props
      ), l & /*$mergedProps*/
      1 && A(O(
        /*$mergedProps*/
        n[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          n[1]
        )
      }, l & /*$mergedProps*/
      1 && {
        name: (
          /*$mergedProps*/
          n[0].value
        )
      }, l & /*$Iconfont*/
      4 && {
        Iconfont: (
          /*$Iconfont*/
          n[2]
        )
      }]) : {};
      t.$set(a);
    },
    i(n) {
      o || (C(t.$$.fragment, n), o = !0);
    },
    o(n) {
      I(t.$$.fragment, n), o = !1;
    },
    d(n) {
      ae(t, n);
    }
  };
}
function we(e) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function Ce(e) {
  let t, o, s = (
    /*$mergedProps*/
    e[0].visible && R(e)
  );
  return {
    c() {
      s && s.c(), t = F();
    },
    m(i, n) {
      s && s.m(i, n), L(i, t, n), o = !0;
    },
    p(i, [n]) {
      /*$mergedProps*/
      i[0].visible ? s ? (s.p(i, n), n & /*$mergedProps*/
      1 && C(s, 1)) : (s = R(i), s.c(), C(s, 1), s.m(t.parentNode, t)) : s && (fe(), I(s, 1, 1, () => {
        s = null;
      }), ce());
    },
    i(i) {
      o || (C(s), o = !0);
    },
    o(i) {
      I(s), o = !1;
    },
    d(i) {
      i && D(t), s && s.d(i);
    }
  };
}
function ke(e, t, o) {
  let s, i, n, l;
  const a = Z(() => import("./icon-tqZnWzZ3.js"));
  let {
    gradio: r
  } = t, {
    props: _ = {}
  } = t;
  const p = g(_);
  K(e, p, (c) => o(17, s = c));
  let {
    _internal: f = {}
  } = t, {
    value: d = ""
  } = t, {
    as_item: u
  } = t, {
    visible: h = !0
  } = t, {
    elem_id: k = ""
  } = t, {
    elem_classes: v = []
  } = t, {
    elem_style: x = {}
  } = t;
  const N = ie();
  K(e, N, (c) => o(2, l = c));
  const [z, M] = T({
    gradio: r,
    props: s,
    _internal: f,
    value: d,
    visible: h,
    elem_id: k,
    elem_classes: v,
    elem_style: x,
    as_item: u
  });
  K(e, z, (c) => o(0, i = c));
  const E = J();
  return K(e, E, (c) => o(1, n = c)), e.$$set = (c) => {
    "gradio" in c && o(8, r = c.gradio), "props" in c && o(9, _ = c.props), "_internal" in c && o(10, f = c._internal), "value" in c && o(11, d = c.value), "as_item" in c && o(12, u = c.as_item), "visible" in c && o(13, h = c.visible), "elem_id" in c && o(14, k = c.elem_id), "elem_classes" in c && o(15, v = c.elem_classes), "elem_style" in c && o(16, x = c.elem_style);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    512 && p.update((c) => ({
      ...c,
      ..._
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, value, visible, elem_id, elem_classes, elem_style, as_item*/
    261376 && M({
      gradio: r,
      props: s,
      _internal: f,
      value: d,
      visible: h,
      elem_id: k,
      elem_classes: v,
      elem_style: x,
      as_item: u
    });
  }, [i, n, l, a, p, N, z, E, r, _, f, d, u, h, k, v, x, s];
}
class Ke extends le {
  constructor(t) {
    super(), de(this, t, ke, Ce, pe, {
      gradio: 8,
      props: 9,
      _internal: 10,
      value: 11,
      as_item: 12,
      visible: 13,
      elem_id: 14,
      elem_classes: 15,
      elem_style: 16
    });
  }
  get gradio() {
    return this.$$.ctx[8];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), b();
  }
  get props() {
    return this.$$.ctx[9];
  }
  set props(t) {
    this.$$set({
      props: t
    }), b();
  }
  get _internal() {
    return this.$$.ctx[10];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), b();
  }
  get value() {
    return this.$$.ctx[11];
  }
  set value(t) {
    this.$$set({
      value: t
    }), b();
  }
  get as_item() {
    return this.$$.ctx[12];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), b();
  }
  get visible() {
    return this.$$.ctx[13];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[14];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[15];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[16];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), b();
  }
}
export {
  Ke as I,
  ve as g,
  g as w
};
